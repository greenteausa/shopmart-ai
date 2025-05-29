'use client'

import { ArrowRight, Heart, Star, TrendingUp } from 'lucide-react'
import { useState } from 'react'

interface RecommendationCardProps {
  title: string
  price: string
  reason: string
  image?: string
}

export default function RecommendationCard({ title, price, reason, image }: RecommendationCardProps) {
  const [isLiked, setIsLiked] = useState(false)
  const [isHovered, setIsHovered] = useState(false)
  
  const defaultImage = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=48&h=48&fit=crop&crop=center'
  
  const getReasonIcon = (reason: string) => {
    if (reason.toLowerCase().includes('popular')) return <TrendingUp className="w-4 h-4 text-orange-500" />
    if (reason.toLowerCase().includes('together')) return <Heart className="w-4 h-4 text-pink-500" />
    if (reason.toLowerCase().includes('rated')) return <Star className="w-4 h-4 text-yellow-500" />
    return <TrendingUp className="w-4 h-4 text-primary-500" />
  }
  
  const getReasonColor = (reason: string) => {
    if (reason.toLowerCase().includes('popular')) return 'bg-orange-100 text-orange-700'
    if (reason.toLowerCase().includes('together')) return 'bg-pink-100 text-pink-700'
    if (reason.toLowerCase().includes('rated')) return 'bg-yellow-100 text-yellow-700'
    return 'bg-primary-100 text-primary-700'
  }
  
  return (
    <div 
      className="card p-5 hover:shadow-xl transition-all duration-300 group cursor-pointer relative overflow-hidden"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background gradient on hover */}
      <div className={`absolute inset-0 bg-gradient-to-r from-primary-50 to-secondary-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300`}></div>
      
      <div className="relative z-10 flex items-center space-x-4">
        <div className="relative">
          <div className="w-16 h-16 bg-gradient-to-br from-neutral-100 to-neutral-200 rounded-2xl flex-shrink-0 overflow-hidden group-hover:scale-110 transition-transform duration-300 shadow-md">
            <img 
              src={image || defaultImage} 
              alt={title}
              className="w-full h-full object-cover rounded-2xl"
            />
          </div>
          
          {/* Floating like button */}
          <button
            onClick={(e) => {
              e.stopPropagation()
              setIsLiked(!isLiked)
            }}
            className={`absolute -top-2 -right-2 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 ${
              isLiked 
                ? 'bg-red-500 text-white scale-110' 
                : 'bg-white text-neutral-400 hover:text-red-500 hover:scale-110 shadow-md'
            }`}
          >
            <Heart className={`w-4 h-4 ${isLiked ? 'fill-current' : ''}`} />
          </button>
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-bold text-neutral-900 text-lg line-clamp-1 group-hover:text-primary-600 transition-colors">
              {title}
            </h4>
          </div>
          
          <div className="flex items-center space-x-3 mb-3">
            <p className="text-xl font-bold text-green-600">{price}</p>
            <div className="flex items-center space-x-1">
              {[...Array(5)].map((_, i) => (
                <Star 
                  key={i} 
                  className={`w-3 h-3 ${
                    i < 4 ? 'text-yellow-400 fill-current' : 'text-neutral-300'
                  }`} 
                />
              ))}
              <span className="text-xs text-neutral-500 ml-1">4.0</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-medium ${getReasonColor(reason)}`}>
              {getReasonIcon(reason)}
              <span>{reason}</span>
            </div>
            
            <div className={`transform transition-all duration-300 ${isHovered ? 'translate-x-1' : ''}`}>
              <ArrowRight className="w-5 h-5 text-primary-500 group-hover:text-primary-600" />
            </div>
          </div>
        </div>
      </div>
      
      {/* Animated border */}
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-primary-500 via-secondary-500 to-accent-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300" style={{ margin: '-1px', zIndex: -1 }}>
        <div className="w-full h-full bg-white rounded-3xl"></div>
      </div>
    </div>
  )
} 