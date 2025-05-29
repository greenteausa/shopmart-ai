'use client'

import { useState, useRef, useEffect } from 'react'
import { Search, Send, ArrowLeft, Loader2, Star, ExternalLink, Filter, SortAsc, Heart, Share, Sparkles } from 'lucide-react'

interface Product {
  name: string
  price: number
  currency: string
  source: string
  source_url: string
  image_url?: string
  rating?: number
  review_count?: number
  key_features: string[]
  availability: boolean
}

interface SearchResult {
  query: string
  products: Product[]
  price_analysis: any
  category_insights: string
  buying_recommendation: string
  search_id: number
}

interface SearchInterfaceProps {
  userId: number | null
  initialQuery?: string
}

export default function SearchInterface({ userId, initialQuery = '' }: SearchInterfaceProps) {
  const [query, setQuery] = useState(initialQuery)
  const [isSearching, setIsSearching] = useState(false)
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null)
  const [chatMessages, setChatMessages] = useState<Array<{type: 'user' | 'assistant', message: string}>>([])
  const [chatInput, setChatInput] = useState('')
  const [isChatMode, setIsChatMode] = useState(false)
  const [isChatting, setIsChatting] = useState(false)
  const [favoriteProducts, setFavoriteProducts] = useState<string[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatMessages])

  useEffect(() => {
    if (initialQuery && !isSearching && !searchResult) {
      handleSearch()
    }
  }, [initialQuery])

  const handleProductClick = (product: Product) => {
    // Open product URL in new tab
    if (product.source_url) {
      window.open(product.source_url, '_blank', 'noopener,noreferrer')
    }
  }

  const handleExternalLink = (e: React.MouseEvent, product: Product) => {
    e.stopPropagation()
    if (product.source_url) {
      window.open(product.source_url, '_blank', 'noopener,noreferrer')
    }
  }

  const handleFavorite = (e: React.MouseEvent, productName: string) => {
    e.stopPropagation()
    setFavoriteProducts(prev => 
      prev.includes(productName)
        ? prev.filter(name => name !== productName)
        : [...prev, productName]
    )
  }

  const handleShare = async (e: React.MouseEvent, product: Product) => {
    e.stopPropagation()
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: product.name,
          text: `Check out this ${product.name} for ${product.currency === 'USD' ? '$' : ''}${product.price}`,
          url: product.source_url
        })
      } catch (error) {
        // Fallback to clipboard
        copyToClipboard(product)
      }
    } else {
      // Fallback to clipboard
      copyToClipboard(product)
    }
  }

  const copyToClipboard = async (product: Product) => {
    const shareText = `${product.name} - ${product.currency === 'USD' ? '$' : ''}${product.price} at ${product.source}\n${product.source_url}`
    
    try {
      await navigator.clipboard.writeText(shareText)
      // You could add a toast notification here
      console.log('Copied to clipboard!')
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  const handleSearch = async () => {
    if (!query.trim()) return
    
    setIsSearching(true)
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: query.trim(), 
          user_id: userId,
          max_rounds: 3 
        })
      })
      
      if (response.ok) {
        const result = await response.json()
        setSearchResult(result)
        setIsChatMode(true)
        setChatMessages([{
          type: 'assistant',
          message: `Found ${result.products.length} products for "${query}". ${result.buying_recommendation}`
        }])
      }
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const handleChat = async () => {
    if (!chatInput.trim() || !searchResult) return
    
    const userMessage = chatInput.trim()
    setChatInput('')
    setChatMessages(prev => [...prev, { type: 'user', message: userMessage }])
    setIsChatting(true)
    
    try {
      const response = await fetch('/api/search/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          search_id: searchResult.search_id,
          message: userMessage,
          user_id: userId
        })
      })
      
      if (response.ok) {
        const result = await response.json()
        setChatMessages(prev => [...prev, { type: 'assistant', message: result.response }])
      }
    } catch (error) {
      console.error('Chat failed:', error)
      setChatMessages(prev => [...prev, { type: 'assistant', message: 'Sorry, I had trouble processing your request.' }])
    } finally {
      setIsChatting(false)
    }
  }

  const goBack = () => {
    setSearchResult(null)
    setIsChatMode(false)
    setChatMessages([])
    setQuery('')
  }

  if (isChatMode && searchResult) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-primary-50/30 flex flex-col">
        {/* Header */}
        <div className="safe-top bg-white/80 backdrop-blur-xl border-b border-neutral-200/50 px-6 py-4 sticky top-0 z-50">
          <div className="flex items-center justify-between slide-up">
            <div className="flex items-center">
              <button onClick={goBack} className="mr-4 p-2 rounded-xl hover:bg-neutral-100 transition-colors">
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="font-bold text-neutral-900 text-lg">Search Results</h1>
                <p className="text-sm text-neutral-600">"{searchResult.query}"</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button className="p-2 rounded-xl hover:bg-neutral-100 transition-colors">
                <Filter className="w-5 h-5 text-neutral-600" />
              </button>
              <button className="p-2 rounded-xl hover:bg-neutral-100 transition-colors">
                <SortAsc className="w-5 h-5 text-neutral-600" />
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="flex-1 overflow-y-auto scrollbar-hide">
          {/* Price Analysis Card */}
          <div className="p-6 slide-up animation-delay-200">
            <div className="card p-6 mb-6">
              <h3 className="font-bold text-lg mb-3 text-gradient">Price Analysis</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-600">${searchResult.price_analysis?.lowest_price || 'N/A'}</p>
                  <p className="text-sm text-neutral-600">Lowest Price</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-primary-600">${searchResult.price_analysis?.average_price || 'N/A'}</p>
                  <p className="text-sm text-neutral-600">Average Price</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-red-600">${searchResult.price_analysis?.highest_price || 'N/A'}</p>
                  <p className="text-sm text-neutral-600">Highest Price</p>
                </div>
              </div>
            </div>
          </div>

          {/* Products Grid */}
          <div className="px-6 pb-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-neutral-900">Products ({searchResult.products.length})</h2>
              <p className="text-sm text-neutral-500">Best matches first</p>
            </div>
            <div className="space-y-4">
              {searchResult.products.map((product, index) => (
                <div 
                  key={index} 
                  className="card p-6 slide-up group hover:scale-[1.02] transition-all duration-300 cursor-pointer"
                  style={{ animationDelay: `${index * 100}ms` }}
                  onClick={() => handleProductClick(product)}
                >
                  <div className="flex space-x-4">
                    <div className="w-20 h-20 bg-neutral-100 rounded-2xl flex items-center justify-center overflow-hidden flex-shrink-0">
                      {product.image_url ? (
                        <img 
                          src={product.image_url} 
                          alt={product.name} 
                          className="w-full h-full object-cover rounded-2xl"
                        />
                      ) : (
                        <Search className="w-8 h-8 text-neutral-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-neutral-900 text-lg mb-1 line-clamp-2 group-hover:text-primary-600 transition-colors">{product.name}</h3>
                      <div className="flex items-center space-x-3 mb-2">
                        <p className="text-2xl font-bold text-primary-600">
                          {product.currency === 'USD' ? '$' : ''}{product.price}
                        </p>
                        <span className="px-3 py-1 bg-primary-100 text-primary-700 text-sm font-medium rounded-full">
                          {product.source}
                        </span>
                        {!product.availability && (
                          <span className="px-2 py-1 bg-red-100 text-red-600 text-xs font-medium rounded-full">
                            Out of Stock
                          </span>
                        )}
                      </div>
                      {product.rating && (
                        <div className="flex items-center mb-3">
                          <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                              <Star 
                                key={i} 
                                className={`w-4 h-4 ${
                                  i < Math.floor(product.rating!) 
                                    ? 'text-yellow-400 fill-current' 
                                    : 'text-neutral-300'
                                }`} 
                              />
                            ))}
                          </div>
                          <span className="text-sm text-neutral-600 ml-2">
                            {product.rating} ({product.review_count} reviews)
                          </span>
                        </div>
                      )}
                      {product.key_features.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {product.key_features.slice(0, 3).map((feature, idx) => (
                            <span key={idx} className="px-2 py-1 bg-neutral-100 text-xs rounded-lg text-neutral-600">
                              {feature}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    <div className="flex flex-col space-y-2">
                      <button 
                        onClick={(e) => handleExternalLink(e, product)}
                        className="p-3 text-primary-600 hover:bg-primary-50 rounded-xl transition-colors group/btn"
                        title="View Product"
                      >
                        <ExternalLink className="w-5 h-5 group-hover/btn:scale-110 transition-transform" />
                      </button>
                      <button 
                        onClick={(e) => handleFavorite(e, product.name)}
                        className={`p-3 rounded-xl transition-colors group/btn ${
                          favoriteProducts.includes(product.name)
                            ? 'text-red-500 bg-red-50'
                            : 'text-neutral-600 hover:bg-red-50 hover:text-red-500'
                        }`}
                        title={favoriteProducts.includes(product.name) ? 'Remove from favorites' : 'Add to favorites'}
                      >
                        <Heart className={`w-5 h-5 group-hover/btn:scale-110 transition-transform ${
                          favoriteProducts.includes(product.name) ? 'fill-current' : ''
                        }`} />
                      </button>
                      <button 
                        onClick={(e) => handleShare(e, product)}
                        className="p-3 text-neutral-600 hover:bg-neutral-100 rounded-xl transition-colors group/btn"
                        title="Share Product"
                      >
                        <Share className="w-5 h-5 group-hover/btn:scale-110 transition-transform" />
                      </button>
                    </div>
                  </div>
                  
                  {/* Click indicator */}
                  <div className="mt-4 pt-3 border-t border-neutral-100 opacity-0 group-hover:opacity-100 transition-opacity">
                    <p className="text-xs text-neutral-500 text-center">
                      Click to view product details →
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Chat Messages */}
          <div className="px-6 pb-6">
            <div className="card p-6">
              <h3 className="font-bold text-lg mb-4 flex items-center">
                <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl mr-3 flex items-center justify-center">
                  💬
                </div>
                Chat with AI Assistant
              </h3>
              <div className="space-y-4 mb-6 max-h-80 overflow-y-auto scrollbar-hide">
                {chatMessages.map((msg, index) => (
                  <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`
                      max-w-[85%] px-4 py-3 rounded-2xl slide-up
                      ${msg.type === 'user' 
                        ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white' 
                        : 'bg-neutral-100 text-neutral-800'
                      }
                    `} style={{ animationDelay: `${index * 100}ms` }}>
                      <p className="text-sm leading-relaxed">{msg.message}</p>
                    </div>
                  </div>
                ))}
                {isChatting && (
                  <div className="flex justify-start">
                    <div className="bg-neutral-100 px-4 py-3 rounded-2xl">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce animation-delay-200"></div>
                        <div className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce animation-delay-400"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>
          </div>
        </div>

        {/* Chat Input */}
        <div className="safe-bottom bg-white/80 backdrop-blur-xl border-t border-neutral-200/50 p-6 sticky bottom-0">
          <div className="flex space-x-3">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !isChatting && handleChat()}
              placeholder="Ask me anything about these products..."
              className="input flex-1"
              disabled={isChatting}
            />
            <button
              onClick={handleChat}
              disabled={!chatInput.trim() || isChatting}
              className="btn-primary p-4"
            >
              {isChatting ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-mesh relative">
      {/* Header */}
      <div className="safe-top px-6 pt-6 pb-4 relative z-10">
        <div className="flex items-center slide-up">
          <button onClick={goBack} className="mr-4 p-2 rounded-xl hover:bg-white/50 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gradient">Search Products</h1>
            <p className="text-neutral-600">Discover the perfect items for you</p>
          </div>
        </div>
      </div>

      {/* Search Interface */}
      <div className="px-6 relative z-10">
        <div className="slide-up animation-delay-200">
          <div className="flex space-x-3 mb-8">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search for anything..."
              className="input flex-1 search-pulse"
              disabled={isSearching}
            />
            <button
              onClick={handleSearch}
              disabled={!query.trim() || isSearching}
              className="btn-primary p-4"
            >
              {isSearching ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Search className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        {/* Search Status */}
        {isSearching && (
          <div className="card p-8 text-center mb-8 slide-up animation-delay-400">
            <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <Loader2 className="w-8 h-8 animate-spin text-white" />
            </div>
            <h3 className="font-bold text-lg text-neutral-900 mb-2">Searching...</h3>
            <p className="text-neutral-600 mb-2">AI is analyzing thousands of products</p>
            <p className="text-sm text-neutral-500">This may take a few moments</p>
            <div className="w-full bg-neutral-200 rounded-full h-2 mt-4">
              <div className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full shimmer"></div>
            </div>
          </div>
        )}

        {/* Quick Search Suggestions */}
        {!isSearching && (
          <div className="slide-up animation-delay-600">
            <h3 className="text-lg font-semibold text-neutral-900 mb-6 flex items-center">
              <Sparkles className="w-5 h-5 mr-2 text-accent-500" />
              Popular Searches
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {[
                { name: 'iPhone 15 Pro', icon: '📱', category: 'Electronics' },
                { name: 'MacBook Air', icon: '💻', category: 'Computers' },
                { name: 'AirPods Pro', icon: '🎧', category: 'Audio' },
                { name: 'iPad Air', icon: '📱', category: 'Tablets' },
                { name: 'Apple Watch', icon: '⌚', category: 'Wearables' },
                { name: 'Nintendo Switch', icon: '🎮', category: 'Gaming' }
              ].map((suggestion, index) => (
                <button
                  key={suggestion.name}
                  onClick={() => setQuery(suggestion.name)}
                  className="card p-4 text-left hover:shadow-xl transition-all group"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl group-hover:scale-110 transition-transform">
                      {suggestion.icon}
                    </div>
                    <div>
                      <p className="font-semibold text-neutral-800">{suggestion.name}</p>
                      <p className="text-sm text-neutral-500">{suggestion.category}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="safe-bottom h-20"></div>
    </div>
  )
} 