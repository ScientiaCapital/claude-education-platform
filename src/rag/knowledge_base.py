import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain.schema import Document
from typing import List, Dict, Any
import json
import hashlib
from config.settings import settings

class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.collection = self.client.get_or_create_collection(
            name="education_kb",
            metadata={"description": "Educational content knowledge base"}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        self.llm = ChatAnthropic(
            model=settings.claude_model,
            temperature=settings.temperature,
            api_key=settings.anthropic_api_key
        )
    
    def add_documents(self, unified_content: List[Dict[str, str]]):
        """Add documents to knowledge base with deduplication"""
        documents = []
        metadatas = []
        ids = []
        
        for content in unified_content:
            if not content.get("content"):
                continue
                
            # Create unique ID based on content hash
            content_hash = hashlib.md5(
                content["content"].encode('utf-8')
            ).hexdigest()
            
            # Split into chunks
            chunks = self.text_splitter.split_text(content["content"])
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{content_hash}_{i}"
                
                # Check if already exists
                existing = self.collection.get(ids=[chunk_id])
                if existing["ids"]:
                    continue
                
                documents.append(chunk)
                metadatas.append({
                    "source": content["source"],
                    "title": content["title"],
                    "url": content.get("url", ""),
                    "chunk_index": i
                })
                ids.append(chunk_id)
        
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Added {len(documents)} chunks to knowledge base")
    
    def search(self, query: str, n_results: int = settings.top_k_results) -> List[Dict]:
        """Search knowledge base"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if results["distances"] else None
            })
        
        return formatted_results
    
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """Generate answer using RAG"""
        context = "\n\n".join([
            f"Source: {doc['metadata']['title']}\nContent: {doc['content']}"
            for doc in context_docs
        ])
        
        prompt = f"""
Based on the following context, answer the question. Be educational and engaging for students learning about AI and programming.

Context:
{context}

Question: {query}

Answer:"""
        
        response = self.llm.invoke(prompt)
        return response.content