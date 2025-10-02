'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Brain, 
  Trophy, 
  Users, 
  Zap, 
  Star, 
  ArrowRight, 
  Play,
  Target,
  Clock,
  Award,
  ChevronRight,
  Sparkles
} from 'lucide-react'

export default function Home() {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "Smart Questions",
      description: "AI-powered questions that adapt to your knowledge level"
    },
    {
      icon: <Trophy className="w-8 h-8" />,
      title: "Competitions",
      description: "Join live tournaments and compete with players worldwide"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Team Play",
      description: "Create teams and challenge friends in group trivia"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Lightning Rounds",
      description: "Quick-fire questions for adrenaline-pumping action"
    }
  ]

  const stats = [
    { number: "50K+", label: "Active Players" },
    { number: "1M+", label: "Questions" },
    { number: "100+", label: "Categories" },
    { number: "24/7", label: "Available" }
  ]

  const categories = [
    { name: "Science", color: "bg-blue-500", questions: 1250 },
    { name: "History", color: "bg-purple-500", questions: 980 },
    { name: "Sports", color: "bg-green-500", questions: 750 },
    { name: "Movies", color: "bg-red-500", questions: 1100 },
    { name: "Geography", color: "bg-yellow-500", questions: 850 },
    { name: "Music", color: "bg-pink-500", questions: 920 }
  ]

  const sampleQuestions = [
    "What is the capital of Australia?",
    "Who painted the Mona Lisa?",
    "What is the largest planet in our solar system?",
    "In which year did World War II end?",
    "What is the chemical symbol for gold?"
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setIsAnimating(true)
      setTimeout(() => {
        setCurrentQuestion((prev) => (prev + 1) % sampleQuestions.length)
        setIsAnimating(false)
      }, 300)
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-effect">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-2"
            >
              <Brain className="w-8 h-8 text-trivia-green" />
              <span className="text-2xl font-bold text-gray-900">TriviaMaster</span>
            </motion.div>
            
            <motion.div 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="hidden md:flex items-center space-x-8"
            >
              <a href="#features" className="text-gray-700 hover:text-trivia-green transition-colors">Features</a>
              <a href="#categories" className="text-gray-700 hover:text-trivia-green transition-colors">Categories</a>
              <a href="#stats" className="text-gray-700 hover:text-trivia-green transition-colors">Stats</a>
              <button className="btn-primary">Get Started</button>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2, duration: 0.6 }}
                  className="inline-flex items-center px-4 py-2 rounded-full bg-trivia-green/10 text-trivia-green font-semibold"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  New: AI-Powered Questions
                </motion.div>
                
                <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                  Test Your
                  <span className="text-transparent bg-clip-text trivia-gradient"> Knowledge</span>
                </h1>
                
                <p className="text-xl text-gray-600 leading-relaxed">
                  Challenge yourself with thousands of trivia questions. 
                  Compete with friends, climb leaderboards, and become a trivia master!
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary flex items-center justify-center space-x-2 text-lg px-8 py-4"
                >
                  <Play className="w-5 h-5" />
                  <span>Start Playing</span>
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-secondary flex items-center justify-center space-x-2 text-lg px-8 py-4"
                >
                  <Users className="w-5 h-5" />
                  <span>Join Tournament</span>
                </motion.button>
              </div>

              {/* Live Question Preview */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.6 }}
                className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
              >
                <div className="flex items-center space-x-2 mb-4">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-semibold text-gray-600">LIVE QUESTION</span>
                </div>
                
                <motion.div
                  key={currentQuestion}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="text-lg font-semibold text-gray-800"
                >
                  {sampleQuestions[currentQuestion]}
                </motion.div>
                
                <div className="mt-4 flex space-x-2">
                  <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: "100%" }}
                      animate={{ width: "0%" }}
                      transition={{ duration: 3, ease: "linear" }}
                      className="h-full bg-trivia-green"
                    />
                  </div>
                  <span className="text-sm text-gray-500">3s</span>
                </div>
              </motion.div>
            </motion.div>

            {/* Hero Visual */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4, duration: 0.8 }}
              className="relative"
            >
              <div className="relative z-10">
                <div className="bg-white rounded-2xl shadow-2xl p-8 transform rotate-3 hover:rotate-0 transition-transform duration-500">
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-12 h-12 bg-trivia-green rounded-full flex items-center justify-center">
                          <Brain className="w-6 h-6 text-white" />
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-900">TriviaMaster</h3>
                          <p className="text-sm text-gray-500">Round 1 of 5</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-trivia-green">1,250</div>
                        <div className="text-sm text-gray-500">Points</div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="text-lg font-semibold text-gray-800">
                        Which planet is known as the "Red Planet"?
                      </div>
                      
                      <div className="space-y-3">
                        {['Mars', 'Venus', 'Jupiter', 'Saturn'].map((option, index) => (
                          <motion.button
                            key={option}
                            whileHover={{ scale: 1.02 }}
                            className="w-full p-4 text-left border-2 border-gray-200 rounded-lg hover:border-trivia-green hover:bg-trivia-green/5 transition-all duration-200"
                          >
                            <div className="flex items-center space-x-3">
                              <div className="w-6 h-6 border-2 border-gray-300 rounded-full"></div>
                              <span className="font-medium">{option}</span>
                            </div>
                          </motion.button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Floating Elements */}
              <motion.div
                animate={{ y: [-10, 10, -10] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="absolute -top-4 -right-4 w-16 h-16 bg-trivia-orange rounded-full flex items-center justify-center shadow-lg"
              >
                <Trophy className="w-8 h-8 text-white" />
              </motion.div>
              
              <motion.div
                animate={{ y: [10, -10, 10] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="absolute -bottom-4 -left-4 w-12 h-12 bg-trivia-blue rounded-full flex items-center justify-center shadow-lg"
              >
                <Star className="w-6 h-6 text-white" />
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="text-center"
              >
                <div className="text-4xl font-bold text-trivia-green mb-2">{stat.number}</div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose TriviaMaster?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the ultimate trivia platform with cutting-edge features and endless entertainment.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="card p-6 text-center group"
              >
                <motion.div
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  className="w-16 h-16 mx-auto mb-4 bg-trivia-green/10 rounded-full flex items-center justify-center text-trivia-green group-hover:bg-trivia-green group-hover:text-white transition-all duration-300"
                >
                  {feature.icon}
                </motion.div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section id="categories" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Explore Categories</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dive into our vast collection of trivia questions across multiple categories.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category, index) => (
              <motion.div
                key={category.name}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                whileHover={{ scale: 1.05 }}
                className="card p-6 group cursor-pointer"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 ${category.color} rounded-lg flex items-center justify-center`}>
                    <Target className="w-6 h-6 text-white" />
                  </div>
                  <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-trivia-green transition-colors" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-2">{category.name}</h3>
                <p className="text-gray-600 mb-4">{category.questions.toLocaleString()} questions</p>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">Start Playing</span>
                  <ArrowRight className="w-4 h-4 text-trivia-green" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 trivia-gradient">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <h2 className="text-4xl lg:text-5xl font-bold text-white mb-4">
              Ready to Become a Trivia Master?
            </h2>
            <p className="text-xl text-white/90 max-w-3xl mx-auto">
              Join millions of players worldwide and start your trivia journey today. 
              Free to play, endless fun!
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-white text-trivia-green font-bold py-4 px-8 rounded-lg text-lg hover:bg-gray-100 transition-colors"
              >
                Start Playing Now
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="border-2 border-white text-white font-bold py-4 px-8 rounded-lg text-lg hover:bg-white hover:text-trivia-green transition-all"
              >
                Learn More
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Brain className="w-8 h-8 text-trivia-green" />
                <span className="text-2xl font-bold">TriviaMaster</span>
              </div>
              <p className="text-gray-400">
                The ultimate trivia platform for knowledge seekers and competitive players.
              </p>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Features</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Live Tournaments</li>
                <li>Team Play</li>
                <li>Leaderboards</li>
                <li>Custom Quizzes</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Categories</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Science & Nature</li>
                <li>History & Geography</li>
                <li>Sports & Entertainment</li>
                <li>Arts & Literature</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-bold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li>Twitter</li>
                <li>Discord</li>
                <li>Facebook</li>
                <li>Instagram</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 TriviaMaster. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
