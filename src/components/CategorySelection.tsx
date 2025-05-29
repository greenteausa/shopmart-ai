'use client'

import { useState } from 'react'
import { Check, ShoppingCart, Laptop, Headphones, Gamepad2, Home, Shirt, Heart, Book, Wrench, Sparkles } from 'lucide-react'

interface CategorySelectionProps {
  onComplete: (categories: string[]) => void
}

const categories = [
  { 
    id: 'electronics', 
    name: 'Electronics', 
    icon: Laptop, 
    description: 'Phones, laptops, tablets & more',
    color: 'from-blue-500 to-cyan-500',
    bgColor: 'bg-blue-50',
    popular: true
  },
  { 
    id: 'audio', 
    name: 'Audio & Music', 
    icon: Headphones, 
    description: 'Headphones, speakers, audio gear',
    color: 'from-purple-500 to-pink-500',
    bgColor: 'bg-purple-50',
    popular: true
  },
  { 
    id: 'gaming', 
    name: 'Gaming', 
    icon: Gamepad2, 
    description: 'Consoles, games, accessories',
    color: 'from-green-500 to-emerald-500',
    bgColor: 'bg-green-50',
    popular: true
  },
  { 
    id: 'home', 
    name: 'Home & Kitchen', 
    icon: Home, 
    description: 'Appliances, furniture, decor',
    color: 'from-orange-500 to-red-500',
    bgColor: 'bg-orange-50',
    popular: false
  },
  { 
    id: 'fashion', 
    name: 'Fashion', 
    icon: Shirt, 
    description: 'Clothing, shoes, accessories',
    color: 'from-pink-500 to-rose-500',
    bgColor: 'bg-pink-50',
    popular: false
  },
  { 
    id: 'health', 
    name: 'Health & Beauty', 
    icon: Heart, 
    description: 'Skincare, fitness, wellness',
    color: 'from-red-500 to-pink-500',
    bgColor: 'bg-red-50',
    popular: false
  },
  { 
    id: 'books', 
    name: 'Books & Media', 
    icon: Book, 
    description: 'Books, movies, educational',
    color: 'from-indigo-500 to-purple-500',
    bgColor: 'bg-indigo-50',
    popular: false
  },
  { 
    id: 'tools', 
    name: 'Tools & Hardware', 
    icon: Wrench, 
    description: 'Tools, hardware, automotive',
    color: 'from-gray-600 to-gray-800',
    bgColor: 'bg-gray-50',
    popular: false
  }
]

export default function CategorySelection({ onComplete }: CategorySelectionProps) {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [step, setStep] = useState(1)

  const toggleCategory = (categoryId: string) => {
    setSelectedCategories(prev => 
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    )
  }

  const handleContinue = () => {
    if (selectedCategories.length === 0) return
    
    if (step === 1) {
      setStep(2)
    } else {
      onComplete(selectedCategories)
    }
  }

  const popularCategories = categories.filter(cat => cat.popular)
  const allCategories = categories

  return (
    <div className="min-h-screen gradient-mesh relative overflow-hidden">
      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 bg-primary-200/20 rounded-full floating animation-delay-200"></div>
        <div className="absolute top-60 right-16 w-24 h-24 bg-secondary-200/20 rounded-full floating animation-delay-400"></div>
        <div className="absolute bottom-40 left-20 w-20 h-20 bg-accent-200/20 rounded-full floating animation-delay-600"></div>
        <div className="absolute top-40 right-32 w-16 h-16 bg-primary-300/20 rounded-full floating animation-delay-800"></div>
      </div>

      <div className="safe-top px-6 py-8 relative z-10">
        {/* Header */}
        <div className="text-center mb-8 slide-up">
          <div className="w-24 h-24 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl flex items-center justify-center mx-auto mb-6 floating shadow-xl">
            <ShoppingCart className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-neutral-900 mb-3 leading-tight">
            Welcome to <span className="text-gradient handwriting text-5xl">ShopMart!</span>
          </h1>
          <p className="text-neutral-600 text-lg leading-relaxed max-w-md mx-auto">
            Let's personalize your shopping experience by selecting your interests
          </p>
        </div>

        {/* Progress Indicator */}
        <div className="flex justify-center mb-8 slide-up animation-delay-200">
          <div className="flex items-center space-x-4">
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
              step >= 1 ? 'bg-primary-500 scale-125' : 'bg-neutral-300'
            }`}></div>
            <div className={`w-8 h-1 rounded-full transition-all duration-300 ${
              step >= 2 ? 'bg-primary-500' : 'bg-neutral-300'
            }`}></div>
            <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
              step >= 2 ? 'bg-primary-500 scale-125' : 'bg-neutral-300'
            }`}></div>
          </div>
        </div>

        {/* Step Content */}
        {step === 1 && (
          <div className="slide-up animation-delay-400">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-neutral-900 mb-2">
                What interests you most?
              </h2>
              <p className="text-neutral-600">Select your favorite shopping categories</p>
            </div>

            {/* Popular Categories */}
            <div className="mb-8">
              <div className="flex items-center justify-center mb-6">
                <div className="flex items-center bg-gradient-to-r from-yellow-100 to-orange-100 px-4 py-2 rounded-full">
                  <Sparkles className="w-4 h-4 text-orange-500 mr-2" />
                  <span className="text-sm font-semibold text-orange-700">Popular Choices</span>
                </div>
              </div>
              
              <div className="grid grid-cols-1 gap-4">
                {popularCategories.map((category, index) => {
                  const Icon = category.icon
                  const isSelected = selectedCategories.includes(category.id)
                  
                  return (
                    <button
                      key={category.id}
                      onClick={() => toggleCategory(category.id)}
                      className={`
                        card p-6 text-left transition-all duration-300 group hover:scale-[1.02] relative overflow-hidden
                        ${isSelected ? 'ring-4 ring-primary-500/50 bg-white shadow-xl' : 'hover:shadow-xl'}
                      `}
                      style={{ animationDelay: `${index * 150}ms` }}
                    >
                      {/* Selection indicator */}
                      {isSelected && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                          <Check className="w-5 h-5 text-white" />
                        </div>
                      )}
                      
                      <div className="flex items-center space-x-4">
                        <div className={`w-16 h-16 bg-gradient-to-r ${category.color} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform shadow-lg`}>
                          <Icon className="w-8 h-8 text-white" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-neutral-900 group-hover:text-primary-600 transition-colors">
                            {category.name}
                          </h3>
                          <p className="text-neutral-600 text-sm mt-1">{category.description}</p>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Continue Button */}
            <div className="text-center">
              <button
                onClick={handleContinue}
                disabled={selectedCategories.length === 0}
                className={`btn-primary text-lg px-8 py-4 shadow-xl transition-all ${
                  selectedCategories.length === 0 
                    ? 'opacity-50 cursor-not-allowed' 
                    : 'hover:shadow-2xl hover:scale-105'
                }`}
              >
                Continue ({selectedCategories.length} selected)
              </button>
              <p className="text-xs text-neutral-500 mt-3">
                You can always change these later
              </p>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="slide-up">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-neutral-900 mb-2">
                Any other interests?
              </h2>
              <p className="text-neutral-600">Add more categories to get better recommendations</p>
            </div>

            {/* All Categories */}
            <div className="grid grid-cols-2 gap-4 mb-8">
              {allCategories.filter(cat => !cat.popular).map((category, index) => {
                const Icon = category.icon
                const isSelected = selectedCategories.includes(category.id)
                
                return (
                  <button
                    key={category.id}
                    onClick={() => toggleCategory(category.id)}
                    className={`
                      card p-4 text-center transition-all duration-300 group hover:scale-[1.02] relative
                      ${isSelected ? 'ring-4 ring-primary-500/50 bg-white shadow-xl' : 'hover:shadow-lg'}
                    `}
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    {/* Selection indicator */}
                    {isSelected && (
                      <div className="absolute top-2 right-2 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center">
                        <Check className="w-4 h-4 text-white" />
                      </div>
                    )}
                    
                    <div className={`w-12 h-12 bg-gradient-to-r ${category.color} rounded-xl flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform shadow-md`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-sm text-neutral-900 group-hover:text-primary-600 transition-colors">
                      {category.name}
                    </h3>
                  </button>
                )
              })}
            </div>

            {/* Complete Setup */}
            <div className="text-center space-y-4">
              <button
                onClick={handleContinue}
                className="btn-primary text-lg px-8 py-4 shadow-xl hover:shadow-2xl hover:scale-105"
              >
                Complete Setup
              </button>
              <button
                onClick={() => setStep(1)}
                className="btn-ghost text-sm"
              >
                ← Back to popular categories
              </button>
            </div>
          </div>
        )}

        {/* Selected Summary */}
        {selectedCategories.length > 0 && (
          <div className="fixed bottom-6 left-6 right-6 z-20">
            <div className="card p-4 bg-white/95 backdrop-blur-xl shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center">
                    <Check className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-neutral-900">
                      {selectedCategories.length} categories selected
                    </p>
                    <p className="text-xs text-neutral-600">
                      {selectedCategories.slice(0, 3).map(id => 
                        categories.find(cat => cat.id === id)?.name
                      ).join(', ')}
                      {selectedCategories.length > 3 && ` +${selectedCategories.length - 3} more`}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="safe-bottom h-20"></div>
    </div>
  )
} 