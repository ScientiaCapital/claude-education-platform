'use client'

import { useState } from 'react'
import { useChat } from 'ai/react'
import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'

type TutorType = 'chatbot' | 'model-training' | 'programming'

interface TutorConfig {
  title: string
  description: string
  icon: string
  color: string
}

const tutorConfigs: Record<TutorType, TutorConfig> = {
  'chatbot': {
    title: 'Tutor de Chatbots',
    description: 'Aprende a crear chatbots inteligentes',
    icon: '🤖',
    color: 'bg-blue-500'
  },
  'model-training': {
    title: 'Tutor de IA',
    description: 'Entrena tu primer modelo de inteligencia artificial',
    icon: '🧠',
    color: 'bg-green-500'
  },
  'programming': {
    title: 'Tutor de Programación',
    description: 'Aprende programación aplicada a IA',
    icon: '💻',
    color: 'bg-purple-500'
  }
}

export default function Home() {
  const [selectedTutor, setSelectedTutor] = useState<TutorType>('chatbot')
  const [difficulty, setDifficulty] = useState<'beginner' | 'intermediate' | 'advanced'>('beginner')
  
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    initialMessages: [],
    body: {
      tutorType: selectedTutor,
      difficulty: difficulty
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Bienvenido a Claude Education
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Aprende inteligencia artificial y programación con tutores especializados
        </p>
      </div>

      {/* Tutor Selection */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Elige tu tutor especializado
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {(Object.entries(tutorConfigs) as [TutorType, TutorConfig][]).map(([type, config]) => (
            <motion.div
              key={type}
              className={`tutor-card cursor-pointer ${
                selectedTutor === type ? 'ring-2 ring-education-primary' : ''
              }`}
              onClick={() => setSelectedTutor(type)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="flex items-center mb-3">
                <div className={`${config.color} rounded-full p-3 text-white text-2xl mr-4`}>
                  {config.icon}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {config.title}
                  </h3>
                </div>
              </div>
              <p className="text-gray-600">{config.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Difficulty Selection */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Nivel de dificultad
        </h3>
        <div className="flex space-x-4">
          {(['beginner', 'intermediate', 'advanced'] as const).map((level) => (
            <button
              key={level}
              onClick={() => setDifficulty(level)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                difficulty === level
                  ? 'bg-education-primary text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {level === 'beginner' && 'Principiante'}
              {level === 'intermediate' && 'Intermedio'}
              {level === 'advanced' && 'Avanzado'}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Interface */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Conversación con {tutorConfigs[selectedTutor].title}
          </h3>
          <p className="text-sm text-gray-600">
            Haz una pregunta o pide que te enseñe sobre un tema específico
          </p>
        </div>

        {/* Messages */}
        <div className="h-96 overflow-y-auto mb-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 py-8">
              <p>¡Haz tu primera pregunta para comenzar a aprender!</p>
              <p className="text-sm mt-2">
                Ejemplos: "¿Cómo crear mi primer chatbot?" o "Explícame qué es machine learning"
              </p>
            </div>
          )}
          
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`chat-message ${message.role}`}
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  {message.role === 'user' ? (
                    <div className="w-8 h-8 bg-education-primary rounded-full flex items-center justify-center text-white text-sm font-medium">
                      Tú
                    </div>
                  ) : (
                    <div className="w-8 h-8 bg-education-secondary rounded-full flex items-center justify-center text-white text-sm">
                      {tutorConfigs[selectedTutor].icon}
                    </div>
                  )}
                </div>
                <div className="flex-1">
                  <ReactMarkdown className="prose prose-sm max-w-none">
                    {message.content}
                  </ReactMarkdown>
                </div>
              </div>
            </motion.div>
          ))}
          
          {isLoading && (
            <div className="chat-message assistant">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-education-secondary rounded-full flex items-center justify-center text-white text-sm">
                  {tutorConfigs[selectedTutor].icon}
                </div>
                <div className="loading-dots">Pensando</div>
              </div>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            value={input}
            onChange={handleInputChange}
            placeholder="Haz una pregunta sobre IA o programación..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-education-primary focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-education-primary text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Enviando...' : 'Enviar'}
          </button>
        </form>
      </div>

      {/* Quick Start Tips */}
      <div className="mt-8 bg-education-background rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          💡 Consejos para empezar
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="activity-card">
            <h4 className="font-medium text-gray-900 mb-2">Para Chatbots:</h4>
            <p className="text-sm text-gray-600">
              "¿Cómo crear un chatbot que responda preguntas sobre mi escuela?"
            </p>
          </div>
          <div className="activity-card">
            <h4 className="font-medium text-gray-900 mb-2">Para IA:</h4>
            <p className="text-sm text-gray-600">
              "Quiero entrenar un modelo que reconozca fotos de animales"
            </p>
          </div>
          <div className="activity-card">
            <h4 className="font-medium text-gray-900 mb-2">Para Programación:</h4>
            <p className="text-sm text-gray-600">
              "Enseñame Python para crear aplicaciones de IA"
            </p>
          </div>
          <div className="activity-card">
            <h4 className="font-medium text-gray-900 mb-2">Proyectos:</h4>
            <p className="text-sm text-gray-600">
              "Quiero hacer un proyecto que combine todo lo que aprenda"
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}