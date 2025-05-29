# 🛍️ ShopMart - AI-Powered Shopping Assistant

<div align="center">

![ShopMart Logo](https://img.shields.io/badge/ShopMart-v2.0-blue?style=for-the-badge&logo=shopping-cart)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com/)

**A modern, AI-powered shopping assistant that helps you discover products across thousands of stores with intelligent search, price comparison, and personalized recommendations.**

[🚀 Live Demo](#) • [📖 Documentation](#) • [🐛 Report Bug](#) • [💡 Request Feature](#)

</div>

---

## ✨ Features

### 🤖 **AI-Powered Search**
- **Intelligent Query Analysis**: Advanced LLM integration for understanding search intent
- **Multi-Source Search**: Searches across Amazon, eBay, Best Buy, Walmart, and more
- **Smart Categorization**: Automatically categorizes products for better results
- **Real-time Chat**: Interactive AI assistant for product inquiries

### 💰 **Price Intelligence**
- **Dynamic Price Comparison**: Real-time price analysis across multiple retailers
- **Deal Detection**: Automatic identification of discounts and special offers
- **Price History Tracking**: Monitor price trends over time
- **Smart Alerts**: Get notified when prices drop

### 🎯 **Personalized Experience**
- **Category Preferences**: Customizable shopping categories
- **Smart Recommendations**: AI-driven product suggestions
- **User Behavior Learning**: Adapts to your shopping patterns
- **Wishlist Management**: Save and track favorite products

### 🎨 **Modern UI/UX**
- **Mobile-First Design**: Optimized for all devices
- **Glassmorphism Effects**: Modern, relaxed design language
- **Smooth Animations**: 60fps micro-interactions and transitions
- **Dark/Light Themes**: Adaptive theming support
- **Accessibility**: WCAG 2.1 AA compliant

---

## 🏗️ Architecture

### **Frontend Stack**
```
Next.js 14 (App Router) + TypeScript + Tailwind CSS
├── 🎨 Modern Design System
├── 🔄 Real-time Updates
├── 📱 Mobile-First Responsive
├── ⚡ Optimized Performance
└── 🎯 Accessibility Focused
```

### **Backend Stack**
```
FastAPI + SQLAlchemy + PostgreSQL/SQLite
├── 🤖 LLM Integration (OpenRouter.ai)
├── 🔍 Multi-Source Search Engine
├── 💾 Intelligent Caching
├── 📊 Performance Monitoring
└── 🔒 Security & Rate Limiting
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ 
- **Python** 3.8+
- **OpenRouter API Key** (optional, falls back to mock data)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shop_mart.git
   cd shop_mart
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Create backend/.env
   echo "OPENROUTER_API_KEY=your_api_key_here" > backend/config.env
   
   # Optional: Database URL (defaults to SQLite)
   echo "DATABASE_URL=postgresql://user:pass@localhost/shopmart" >> backend/config.env
   ```

5. **Start Development Servers**
   ```bash
   # Terminal 1: Backend
   cd backend && python main.py
   
   # Terminal 2: Frontend
   npm run dev
   ```

6. **Visit the Application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

## 🎯 Key Optimizations & Features

### **🎨 Frontend Enhancements**

#### **Modern Design System**
- **Glassmorphism UI**: Translucent cards with backdrop blur effects
- **Gradient Animations**: Dynamic color transitions and floating elements
- **Micro-interactions**: Smooth hover states and click animations
- **Typography**: Custom font combinations (Inter + Poppins + Caveat)

#### **Performance Optimizations**
- **Lazy Loading**: Components and images load on demand
- **Code Splitting**: Optimized bundle sizes with Next.js automatic splitting
- **Image Optimization**: WebP format with proper sizing
- **Caching Strategies**: Browser and CDN caching for static assets

#### **UX Improvements**
- **Progressive Onboarding**: Step-by-step category selection
- **Real-time Feedback**: Loading states and progress indicators
- **Error Boundaries**: Graceful error handling and recovery
- **Accessibility**: Screen reader support and keyboard navigation

### **⚡ Backend Optimizations**

#### **Search Engine Enhancements**
- **Intelligent Caching**: 5-minute TTL cache with LRU eviction
- **Rate Limiting**: 100 requests/minute with IP-based throttling
- **Enhanced Algorithms**: Smart product categorization and relevance scoring
- **Mock Data Intelligence**: Realistic product generation with proper pricing

#### **Performance Improvements**
- **Async Processing**: Non-blocking I/O for all search operations
- **Connection Pooling**: Efficient database connection management
- **Response Compression**: GZip compression for API responses
- **Request Logging**: Comprehensive performance monitoring

#### **API Enhancements**
- **Advanced Error Handling**: Detailed error responses with proper HTTP codes
- **API Versioning**: Structured versioning system
- **Documentation**: Auto-generated OpenAPI specs
- **Health Checks**: Comprehensive system status endpoints

---

## 📁 Project Structure

```
shop_mart/
├── 📱 Frontend (Next.js)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Root layout with fonts
│   │   │   ├── page.tsx           # Enhanced homepage
│   │   │   └── globals.css        # Modern design system
│   │   └── components/
│   │       ├── SearchInterface.tsx # AI-powered search
│   │       ├── CategorySelection.tsx # Onboarding flow
│   │       ├── TrendingDeals.tsx   # Deal cards
│   │       └── RecommendationCard.tsx # Product recommendations
│   ├── package.json
│   ├── tailwind.config.js         # Extended design tokens
│   ├── next.config.js             # Image optimization
│   └── tsconfig.json              # TypeScript config
│
├── 🔧 Backend (FastAPI)
│   ├── main.py                    # Enhanced FastAPI app
│   ├── database.py               # SQLAlchemy models
│   ├── search_service.py         # Optimized search engine
│   ├── llm_service.py            # LLM integration
│   ├── routers/
│   │   ├── search.py             # Search endpoints
│   │   ├── users.py              # User management
│   │   ├── products.py           # Product data
│   │   └── recommendations.py     # AI recommendations
│   ├── requirements.txt
│   └── config.env               # Environment variables
│
└── 📄 Documentation
    ├── README.md                # This file
    └── API.md                   # API documentation
```

---

## 🔌 API Endpoints

### **Search & AI**
- `POST /api/search` - Multi-round AI-powered search
- `POST /api/search/chat` - Interactive chat about search results
- `GET /api/search/trending` - Get trending search queries

### **Products**
- `GET /api/products/{id}` - Get detailed product information
- `GET /api/products/{id}/price-history` - Price tracking data
- `POST /api/products/{id}/track` - Start price tracking

### **Users**
- `POST /api/users/register` - User registration
- `PUT /api/users/{id}/preferences` - Update shopping preferences
- `GET /api/users/{id}/history` - Search and purchase history

### **Recommendations**
- `GET /api/recommendations/personalized` - AI-powered recommendations
- `GET /api/recommendations/trending` - Popular products
- `GET /api/recommendations/deals` - Best current deals

---

## 🛠️ Development

### **Environment Variables**

```bash
# Backend Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
DATABASE_URL=sqlite:///./shop_mart.db
ENVIRONMENT=development
LOG_LEVEL=INFO

# Optional: External API Keys
AMAZON_API_KEY=your_amazon_key
EBAY_API_KEY=your_ebay_key
```

### **Development Commands**

```bash
# Frontend Development
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking

# Backend Development
python main.py       # Start development server
pytest              # Run tests
black .             # Code formatting
mypy .              # Type checking
```

### **Docker Deployment**

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🎨 Design Philosophy

### **Visual Design**
- **Glassmorphism**: Modern, frosted glass aesthetic
- **Gradient Mesh**: Dynamic background patterns
- **Micro-animations**: Subtle, purposeful motion
- **Color Psychology**: Calming blues and energetic accents

### **User Experience**
- **Progressive Disclosure**: Information revealed when needed
- **Feedback Loops**: Immediate response to user actions
- **Error Prevention**: Guided flows that prevent mistakes
- **Accessibility First**: Inclusive design for all users

---

## 🔮 Roadmap

### **Phase 1: Core Optimization** ✅
- [x] Modern UI/UX redesign
- [x] Backend performance optimization
- [x] Enhanced search algorithms
- [x] Improved error handling

### **Phase 2: Advanced Features** 🚧
- [ ] Real-time price alerts
- [ ] Social shopping features
- [ ] Advanced analytics dashboard
- [ ] Mobile app development

### **Phase 3: AI Enhancement** 📅
- [ ] Computer vision for product matching
- [ ] Natural language search
- [ ] Predictive recommendations
- [ ] Voice shopping assistant

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenRouter.ai](https://openrouter.ai/) for LLM API services
- [Unsplash](https://unsplash.com/) for beautiful placeholder images
- [Lucide Icons](https://lucide.dev/) for the amazing icon library
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS framework

---

<div align="center">

**Built with ❤️ for smart shoppers everywhere**

[⭐ Star this project](https://github.com/yourusername/shop_mart) if you found it helpful!

</div> 