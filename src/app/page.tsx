'use client'

import { useState, useEffect } from 'react'
import { Search, Sparkles, TrendingUp, Heart, ShoppingBag, Zap, Star, Clock } from 'lucide-react'
import SearchInterface from '@/components/SearchInterface'
import CategorySelection from '@/components/CategorySelection'
import TrendingDeals from '@/components/TrendingDeals'
import RecommendationCard from '@/components/RecommendationCard'

export default function HomePage() {
  const [isFirstTime, setIsFirstTime] = useState(false)
  const [showSearch, setShowSearch] = useState(false)
  const [userId, setUserId] = useState<number | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    // Check if user is first time (in real app, check localStorage/auth)
    const firstTime = !localStorage.getItem('shopmart_user_preferences')
    setIsFirstTime(firstTime)
  }, [])

  const handleCategorySelection = (categories: string[]) => {
    localStorage.setItem('shopmart_user_preferences', JSON.stringify({ categories }))
    setIsFirstTime(false)
  }

  const handleQuickSearch = (query: string) => {
    setSearchQuery(query)
    setShowSearch(true)
  }

  const handleGetStarted = () => {
    setShowSearch(true)
  }

  if (!mounted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex items-center justify-center">
        <div className="text-2xl font-bold text-gradient">ShopMart</div>
      </div>
    )
  }

  if (isFirstTime) {
    return <CategorySelection onComplete={handleCategorySelection} />
  }

  if (showSearch) {
    return <SearchInterface userId={userId} initialQuery={searchQuery} />
  }

  return (
    <div className="min-h-screen gradient-mesh relative overflow-x-hidden">
      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-20 h-20 bg-primary-200/30 rounded-full floating animation-delay-200"></div>
        <div className="absolute top-40 right-16 w-16 h-16 bg-secondary-200/30 rounded-full floating animation-delay-400"></div>
        <div className="absolute bottom-32 left-20 w-12 h-12 bg-accent-200/30 rounded-full floating animation-delay-600"></div>
      </div>

      {/* Header */}
      <div className="safe-top px-6 pt-6 pb-4 relative z-10">
        <div className="flex items-center justify-between slide-up">
          <div>
            <h1 className="text-3xl font-bold text-gradient">ShopMart</h1>
            <p className="text-sm text-neutral-600 font-medium">Your AI shopping companion</p>
          </div>
          <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center shadow-lg floating">
            <ShoppingBag className="w-6 h-6 text-white" />
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="px-6 py-8 relative z-10">
        <div className="text-center slide-up animation-delay-200">
          <div className="w-20 h-20 bg-gradient-to-r from-primary-100 to-secondary-100 rounded-3xl flex items-center justify-center mx-auto mb-6 floating shadow-lg">
            <Sparkles className="w-10 h-10 text-primary-600" />
          </div>
          <h2 className="text-4xl font-bold text-neutral-900 mb-3 leading-tight">
            Discover anything<br />
            <span className="text-gradient handwriting text-5xl">you desire</span>
          </h2>
          <p className="text-neutral-600 mb-8 leading-relaxed max-w-md mx-auto text-lg">
            AI-powered search across thousands of stores with smart price comparison and personalized recommendations.
          </p>
          
          {/* Quick Search Bar */}
          <div className="mb-8 max-w-md mx-auto">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && searchQuery.trim() && handleQuickSearch(searchQuery)}
                placeholder="What are you looking for?"
                className="input pr-14 search-pulse"
              />
              <button
                onClick={() => searchQuery.trim() && handleQuickSearch(searchQuery)}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 btn-primary p-3"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          <button
            onClick={handleGetStarted}
            className="btn-primary text-lg shadow-xl hover:shadow-2xl mb-8"
          >
            <Zap className="w-5 h-5 mr-2" />
            Start Exploring
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="px-6 mb-8 slide-up animation-delay-400">
        <div className="grid grid-cols-2 gap-4">
          <button 
            onClick={() => setShowSearch(true)}
            className="card p-6 text-center hover:shadow-xl transition-all group"
          >
            <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl mx-auto mb-3 flex items-center justify-center group-hover:scale-110 transition-transform">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-neutral-800">Trending Now</p>
            <p className="text-sm text-neutral-500 mt-1">Hot products everyone's buying</p>
          </button>
          <button 
            onClick={() => setShowSearch(true)}
            className="card p-6 text-center hover:shadow-xl transition-all group"
          >
            <div className="w-12 h-12 bg-gradient-to-r from-secondary-500 to-secondary-600 rounded-2xl mx-auto mb-3 flex items-center justify-center group-hover:scale-110 transition-transform">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <p className="font-semibold text-neutral-800">Best Deals</p>
            <p className="text-sm text-neutral-500 mt-1">Unbeatable prices today</p>
          </button>
        </div>
      </div>

      {/* Popular Searches */}
      <div className="px-6 mb-8 slide-up animation-delay-600">
        <h3 className="text-lg font-semibold text-neutral-900 mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2 text-accent-500" />
          Popular Searches
        </h3>
        <div className="flex flex-wrap gap-3">
          {[
            { query: 'iPhone 15 Pro', emoji: '📱' },
            { query: 'MacBook Air', emoji: '💻' },
            { query: 'AirPods Pro', emoji: '🎧' },
            { query: 'Nintendo Switch', emoji: '🎮' },
            { query: 'iPad Air', emoji: '📱' },
            { query: 'Apple Watch', emoji: '⌚' }
          ].map((item, index) => (
            <button
              key={item.query}
              onClick={() => handleQuickSearch(item.query)}
              className="btn-secondary text-sm flex items-center space-x-2 hover:scale-105"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <span>{item.emoji}</span>
              <span>{item.query}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Trending Deals Preview */}
      <div className="px-6 mb-8 slide-up animation-delay-200">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-neutral-900 flex items-center">
            <div className="w-8 h-8 bg-gradient-to-r from-red-500 to-orange-500 rounded-xl mr-3 flex items-center justify-center">
              🔥
            </div>
            Hot Deals
          </h3>
          <div className="flex items-center text-sm text-neutral-500">
            <Clock className="w-4 h-4 mr-1" />
            Limited time
          </div>
        </div>
        <TrendingDeals />
      </div>

      {/* Recommendations Preview */}
      <div className="px-6 pb-8 slide-up animation-delay-400">
        <h3 className="text-xl font-bold text-neutral-900 mb-6 mt-8 flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl mr-3 flex items-center justify-center">
            💡
          </div>
          Just For You
        </h3>
        <div className="space-y-4">
          <RecommendationCard 
            title="iPhone 15 Pro Max"
            price="$999"
            reason="Popular in Electronics"
            image="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=48&h=48&fit=crop&crop=center"
          />
          <RecommendationCard 
            title="AirPods Pro 3"
            price="$249"
            reason="Frequently bought together"
            image="https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=48&h=48&fit=crop&crop=center"
          />
          <RecommendationCard 
            title="MacBook Air M3"
            price="$1,199"
            reason="Top rated in your category"
            image="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=48&h=48&fit=crop&crop=center"
          />
        </div>
      </div>

      {/* Footer */}
      <div className="px-6 pb-8 text-center">
        <p className="text-neutral-400 text-sm">
          Made with <span className="text-red-400">♥</span> for smart shoppers
        </p>
      </div>

      {/* Bottom Navigation Space */}
      <div className="safe-bottom h-20"></div>
    </div>
  )
} 