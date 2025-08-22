#!/usr/bin/env python3
"""
Comprehensive test script for Claude Education Platform
Tests all major components and integrations
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

async def test_database():
    """Test database connection and operations"""
    print_section("Testing Database Connection")
    
    try:
        from src.database.connection import DatabaseManager
        
        db = DatabaseManager()
        await db.connect()
        print("✅ Database connection successful")
        
        # Test a simple query
        result = await db.pool.fetchval("SELECT 1")
        if result == 1:
            print("✅ Database query test passed")
        
        await db.disconnect()
        print("✅ Database disconnection successful")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

async def test_apis():
    """Test API key configurations"""
    print_section("Testing API Configurations")
    
    from config.settings import settings
    
    apis = {
        "Anthropic": bool(settings.anthropic_api_key),
        "Firecrawl": bool(settings.firecrawl_api_key),
        "Exa": bool(settings.exa_api_key),
        "Tavily": bool(settings.tavily_api_key),
        "DeepSeek": bool(settings.deepseek_api_key),
    }
    
    for api, configured in apis.items():
        if configured:
            print(f"✅ {api} API key configured")
        else:
            print(f"⚠️  {api} API key not configured")
    
    return all(apis.values())

def test_imports():
    """Test all major module imports"""
    print_section("Testing Module Imports")
    
    modules_to_test = [
        ("src.tools.data_collector", "DataCollector"),
        ("src.rag.knowledge_base", "KnowledgeBase"),
        ("src.agents.tutor_agent", "ChatbotTutor"),
        ("src.models.deepseek_client", "DeepSeekClient"),
        ("src.tools.enhanced_research", "EnhancedResearchTools"),
    ]
    
    all_passed = True
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✅ {module_path}.{class_name} imported successfully")
        except Exception as e:
            print(f"❌ Failed to import {module_path}.{class_name}: {e}")
            all_passed = False
    
    return all_passed

def test_deepseek():
    """Test DeepSeek client initialization"""
    print_section("Testing DeepSeek Integration")
    
    try:
        from src.models.deepseek_client import DeepSeekClient
        
        client = DeepSeekClient()
        models = client.list_available_models()
        
        print(f"✅ DeepSeek client initialized")
        print(f"✅ Found {len(models)} model configurations")
        
        # Show available models
        for model in models[:3]:  # Show first 3
            status = "Available" if model['available'] else "Not Available"
            print(f"   - {model['name']}: {status}")
        
        return True
    except Exception as e:
        print(f"❌ DeepSeek test failed: {e}")
        return False

def test_frontend():
    """Check frontend build status"""
    print_section("Testing Frontend Build")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if build directory exists
    build_path = frontend_path / ".next"
    if build_path.exists():
        print("✅ Frontend build directory exists")
    else:
        print("⚠️  Frontend not built (run 'npm run build' in frontend/)")
    
    # Check package.json
    package_json = frontend_path / "package.json"
    if package_json.exists():
        print("✅ package.json found")
    else:
        print("❌ package.json not found")
    
    return True

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  CLAUDE EDUCATION PLATFORM - SYSTEM TEST")
    print("="*60)
    
    results = []
    
    # Test imports
    results.append(("Module Imports", test_imports()))
    
    # Test APIs
    results.append(("API Configurations", await test_apis()))
    
    # Test database
    results.append(("Database Connection", await test_database()))
    
    # Test DeepSeek
    results.append(("DeepSeek Integration", test_deepseek()))
    
    # Test frontend
    results.append(("Frontend Build", test_frontend()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("  🎉 ALL TESTS PASSED!")
    else:
        print("  ⚠️  SOME TESTS FAILED - Review output above")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)