'use client'

import { Star, ExternalLink, Timer, Zap } from 'lucide-react'
import { useState } from 'react'

const deals = [
  {
    id: 1,
    name: 'iPhone 15 Pro',
    originalPrice: 1099.99,
    salePrice: 899.99,
    discount: 18,
    source: 'Apple Store',
    rating: 4.8,
    reviewCount: 2847,
    image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=80&h=80&fit=crop&crop=center',
    timeLeft: '2 hours',
    trending: true
  },
  {
    id: 2,
    name: 'MacBook Air M3',
    originalPrice: 1399.99,
    salePrice: 1199.99,
    discount: 14,
    source: 'Best Buy',
    rating: 4.9,
    reviewCount: 1532,
    image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=80&h=80&fit=crop&crop=center',
    timeLeft: '1 day',
    trending: false
  },
  {
    id: 3,
    name: 'AirPods Pro 3',
    originalPrice: 279.99,
    salePrice: 199.99,
    discount: 29,
    source: 'Amazon',
    rating: 4.7,
    reviewCount: 5632,
    image: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=80&h=80&fit=crop&crop=center',
    timeLeft: '6 hours',
    trending: true
  }
]

export default function TrendingDeals() {
  const [likedDeals, setLikedDeals] = useState<number[]>([])

  const toggleLike = (dealId: number) => {
    setLikedDeals(prev => 
      prev.includes(dealId) 
        ? prev.filter(id => id !== dealId)
        : [...prev, dealId]
    )
  }

  return (
    <div className="space-y-4">
      {deals.map((deal, index) => (
        <div 
          key={deal.id} 
          className="card p-6 slide-up hover:scale-[1.02] transition-all duration-300 group relative overflow-hidden"
          style={{ animationDelay: `${index * 150}ms` }}
        >
          {/* Trending Badge */}
          {deal.trending && (
            <div className="absolute top-4 right-4 bg-gradient-to-r from-red-500 to-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full flex items-center">
              <Zap className="w-3 h-3 mr-1" />
              HOT
            </div>
          )}

          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-20 h-20 bg-gradient-to-br from-neutral-100 to-neutral-200 rounded-2xl flex-shrink-0 overflow-hidden group-hover:scale-110 transition-transform duration-300">
                <img 
                  src={deal.image} 
                  alt={deal.name}
                  className="w-full h-full object-cover rounded-2xl"
                />
              </div>
              {deal.discount >= 20 && (
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                  🔥
                </div>
              )}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-bold text-neutral-900 text-lg group-hover:text-primary-600 transition-colors">{deal.name}</h4>
                <button
                  onClick={() => toggleLike(deal.id)}
                  className={`p-2 rounded-xl transition-all ${
                    likedDeals.includes(deal.id)
                      ? 'text-red-500 bg-red-50 scale-110'
                      : 'text-neutral-400 hover:text-red-500 hover:bg-red-50'
                  }`}
                >
                  <svg className="w-5 h-5" fill={likedDeals.includes(deal.id) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </button>
              </div>

              <div className="flex items-center space-x-3 mb-3">
                <div className="flex items-center space-x-2">
                  <span className="text-2xl font-bold text-green-600">
                    ${deal.salePrice}
                  </span>
                  <span className="text-lg text-neutral-500 line-through">
                    ${deal.originalPrice}
                  </span>
                </div>
                <span className="px-3 py-1 bg-gradient-to-r from-red-500 to-red-600 text-white text-sm font-bold rounded-full">
                  -{deal.discount}% OFF
                </span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-4 h-4 ${
                          i < Math.floor(deal.rating) 
                            ? 'text-yellow-400 fill-current' 
                            : 'text-neutral-300'
                        }`} 
                      />
                    ))}
                    <span className="text-sm text-neutral-600 ml-2 font-medium">
                      {deal.rating} ({deal.reviewCount.toLocaleString()})
                    </span>
                  </div>
                </div>
                <div className="flex items-center text-sm text-neutral-500">
                  <Timer className="w-4 h-4 mr-1" />
                  {deal.timeLeft} left
                </div>
              </div>

              <div className="flex items-center justify-between mt-4">
                <span className="text-sm font-medium text-neutral-600 bg-neutral-100 px-3 py-1 rounded-full">
                  {deal.source}
                </span>
                <button className="btn-primary text-sm px-6 py-2 group-hover:shadow-lg">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  View Deal
                </button>
              </div>
            </div>
          </div>

          {/* Progress bar for time urgency */}
          <div className="mt-4 bg-neutral-200 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-red-500 to-orange-500 h-full rounded-full transition-all duration-1000"
              style={{ 
                width: deal.timeLeft.includes('hour') ? '85%' : 
                       deal.timeLeft.includes('day') ? '30%' : '95%' 
              }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  )
} 