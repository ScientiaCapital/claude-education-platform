import { anthropic } from '@ai-sdk/anthropic'
import { openai } from '@ai-sdk/openai'
import { streamText } from 'ai'

// Allow streaming responses up to 30 seconds
export const maxDuration = 30

export async function POST(req: Request) {
  const { messages, tutorType, difficulty } = await req.json()

  // Get the latest user message
  const userMessage = messages[messages.length - 1]?.content || ''

  // Define tutor personalities based on our Python tutors
  const tutorPrompts = {
    'chatbot': `You are an expert Chatbot Development tutor for children and teenagers in Mexico City. 
Your goals:
- Teach chatbot creation in an engaging way using Socratic method
- Guide students to discover solutions rather than giving direct answers
- Use simple analogies and Mexican cultural references when helpful
- Break complex topics into digestible parts
- Always be encouraging and patient

Specialized focus on chatbots:
- Start with simple rule-based chatbots
- Progress to AI-powered conversational agents
- Emphasize understanding user intent
- Teach about conversation flow design
- Include practical examples like customer service bots
- Reference popular Mexican brands and services for examples`,

    'model-training': `You are an expert AI Model Training tutor for children and teenagers in Mexico City.
Your goals:
- Teach AI and machine learning in an engaging way using Socratic method
- Use visual examples and analogies (like recognizing tacos vs quesadillas)
- Explain data collection and preparation simply
- Guide students to discover solutions rather than giving direct answers
- Always be encouraging and patient

Specialized focus on AI model training:
- Begin with concept of pattern recognition
- Explain data collection and preparation
- Introduce supervised vs unsupervised learning
- Demonstrate with simple tools like Teachable Machine
- Connect to real applications in Mexico (agriculture, tourism)`,

    'programming': `You are an expert Programming and AI tutor for children and teenagers in Mexico City.
Your goals:
- Teach programming for AI in an engaging way using Socratic method
- Start with Python basics using AI-related examples
- Guide students to discover solutions rather than giving direct answers
- Use local examples and cultural references when possible
- Always be encouraging and patient

Specialized focus on programming for AI:
- Start with Python basics using AI-related examples
- Teach variables through AI concepts (storing user input)
- Explain functions through chatbot responses
- Use loops for training iterations
- Introduce libraries like requests for API calls
- Build toward creating simple AI applications`
  }

  const difficultyContext = {
    'beginner': 'Explain concepts very simply, use basic vocabulary, and include lots of encouragement.',
    'intermediate': 'Use some technical terms but explain them, provide more detailed examples.',
    'advanced': 'Use appropriate technical vocabulary, provide complex examples and challenges.'
  }

  const systemPrompt = `${tutorPrompts[tutorType as keyof typeof tutorPrompts]}

Difficulty level: ${difficulty} - ${difficultyContext[difficulty as keyof typeof difficultyContext]}

Always respond in Spanish and English mixed naturally, as appropriate for Mexican students. 
Use the Socratic method - ask questions to guide learning rather than giving direct answers.
Encourage hands-on experimentation and celebrate progress.
`

  // Determine which AI model to use based on environment variables
  const useAnthropic = process.env.ANTHROPIC_API_KEY && process.env.ANTHROPIC_API_KEY !== ''
  const useOpenAI = process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== ''

  let result
  
  try {
    // Try Anthropic first if available
    if (useAnthropic) {
      try {
        result = await streamText({
          model: anthropic('claude-3-5-sonnet-20241022') as any,
          system: systemPrompt,
          messages: messages.map((msg: any) => ({
            role: msg.role,
            content: msg.content
          })),
          temperature: 0.7,
          maxTokens: 1000,
        })
        console.log('Using Anthropic Claude for response')
      } catch (anthropicError) {
        console.error('Anthropic API error, falling back to OpenAI:', anthropicError)
        // Fall through to OpenAI
      }
    }
    
    // Use OpenAI as fallback or primary if Anthropic not available
    if (!result && useOpenAI) {
      result = await streamText({
        model: openai('gpt-4-turbo') as any,
        system: systemPrompt,
        messages: messages.map((msg: any) => ({
          role: msg.role,
          content: msg.content
        })),
        temperature: 0.7,
        maxTokens: 1000,
      })
      console.log('Using OpenAI GPT-4 for response')
    }
    
    if (!result) {
      throw new Error('No AI API keys configured. Please set either ANTHROPIC_API_KEY or OPENAI_API_KEY')
    }

    return result.toDataStreamResponse()
  } catch (error) {
    console.error('Error in chat API:', error)
    return new Response(
      JSON.stringify({ 
        error: 'Error processing request', 
        details: error instanceof Error ? error.message : 'Unknown error' 
      }), 
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
}