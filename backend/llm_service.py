import httpx
import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class SearchRound(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    reasoning: str

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "deepseek/deepseek-r1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://shopmart.app",
            "X-Title": "ShopMart"
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def call_llm(self, messages: List[Dict[str, str]], max_tokens: int = 2000) -> str:
        """Make a call to the DeepSeek model via OpenRouter"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]

    async def analyze_user_query(self, query: str) -> Dict[str, Any]:
        """Analyze user query to understand search intent and extract key information"""
        messages = [
            {
                "role": "system",
                "content": """You are a shopping assistant AI. Analyze the user's query to understand what product they're looking for.

Extract and return in JSON format:
{
    "product_name": "main product name",
    "category": "product category",
    "key_features": ["feature1", "feature2"],
    "price_range": {"min": 0, "max": 1000},
    "search_keywords": ["keyword1", "keyword2"],
    "intent": "compare|buy|research|browse",
    "specificity": "high|medium|low"
}"""
            },
            {
                "role": "user", 
                "content": f"Analyze this shopping query: {query}"
            }
        ]
        
        response = await self.call_llm(messages)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "product_name": query,
                "category": "general",
                "key_features": [],
                "price_range": {"min": 0, "max": 10000},
                "search_keywords": [query],
                "intent": "research",
                "specificity": "medium"
            }

    async def generate_search_queries(self, analysis: Dict[str, Any], round_num: int = 1) -> List[str]:
        """Generate multiple search queries for comprehensive product research"""
        messages = [
            {
                "role": "system",
                "content": f"""You are a shopping research expert. Generate {3 + round_num} diverse search queries to find comprehensive information about a product.

For round {round_num}, focus on:
- Round 1: Basic product info, prices, popular retailers
- Round 2: Technical specs, reviews, comparisons
- Round 3: Deals, alternatives, user experiences

Return a JSON array of search query strings."""
            },
            {
                "role": "user",
                "content": f"Product analysis: {json.dumps(analysis)}\nGenerate search queries for round {round_num}"
            }
        ]
        
        response = await self.call_llm(messages)
        try:
            queries = json.loads(response)
            return queries if isinstance(queries, list) else [response]
        except json.JSONDecodeError:
            # Fallback queries
            product_name = analysis.get("product_name", "product")
            return [
                f"{product_name} price comparison",
                f"best {product_name} reviews",
                f"{product_name} specifications features",
                f"where to buy {product_name} online"
            ]

    async def analyze_search_results(self, query: str, search_results: List[Dict], previous_rounds: List[SearchRound] = None) -> Dict[str, Any]:
        """Analyze search results and determine if more rounds are needed"""
        messages = [
            {
                "role": "system",
                "content": """You are a shopping research analyst. Analyze search results and determine:

1. Quality and completeness of information
2. Whether additional search rounds are needed
3. Key insights found
4. Missing information that should be searched for

Return JSON:
{
    "quality_score": 0.8,
    "completeness": "high|medium|low", 
    "key_insights": ["insight1", "insight2"],
    "missing_info": ["missing1", "missing2"],
    "needs_more_rounds": true/false,
    "recommended_next_queries": ["query1", "query2"]
}"""
            },
            {
                "role": "user",
                "content": f"Original query: {query}\nSearch results: {json.dumps(search_results[:5])}\nPrevious rounds: {len(previous_rounds or [])}"
            }
        ]
        
        response = await self.call_llm(messages)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "quality_score": 0.7,
                "completeness": "medium",
                "key_insights": [],
                "missing_info": [],
                "needs_more_rounds": len(previous_rounds or []) < 2,
                "recommended_next_queries": []
            }

    async def generate_product_summary(self, all_results: List[SearchRound]) -> Dict[str, Any]:
        """Generate comprehensive product summary from all search rounds"""
        messages = [
            {
                "role": "system", 
                "content": """You are a shopping expert. Create a comprehensive product summary from search results.

Return JSON with:
{
    "products": [
        {
            "name": "Product Name",
            "brand": "Brand",
            "price": 99.99,
            "currency": "USD",
            "source": "retailer name",
            "source_url": "url",
            "image_url": "image_url",
            "key_features": ["feature1", "feature2"],
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"],
            "rating": 4.5,
            "review_count": 1234,
            "availability": true
        }
    ],
    "price_analysis": {
        "lowest_price": 89.99,
        "highest_price": 129.99,
        "average_price": 104.99,
        "best_deal": "retailer with best value"
    },
    "category_insights": "insights about this product category",
    "buying_recommendation": "expert recommendation"
}"""
            },
            {
                "role": "user",
                "content": f"Analyze these search results and create a product summary: {json.dumps([round.dict() for round in all_results])}"
            }
        ]
        
        response = await self.call_llm(messages, max_tokens=3000)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "products": [],
                "price_analysis": {},
                "category_insights": "No analysis available",
                "buying_recommendation": "Unable to generate recommendation"
            }

    async def generate_recommendations(self, user_preferences: Dict, search_history: List[str]) -> List[Dict[str, Any]]:
        """Generate personalized product recommendations"""
        messages = [
            {
                "role": "system",
                "content": """Generate personalized product recommendations based on user preferences and search history.

Return JSON array of recommendations:
[
    {
        "product_name": "Product Name",
        "category": "category",
        "reason": "why recommended",
        "confidence": 0.85,
        "estimated_price": 99.99
    }
]"""
            },
            {
                "role": "user",
                "content": f"User preferences: {json.dumps(user_preferences)}\nSearch history: {json.dumps(search_history[-10:])}"
            }
        ]
        
        response = await self.call_llm(messages)
        try:
            recommendations = json.loads(response)
            return recommendations if isinstance(recommendations, list) else []
        except json.JSONDecodeError:
            return []

    async def analyze_price_trends(self, price_history: List[Dict]) -> Dict[str, Any]:
        """Analyze price trends and predict future prices"""
        messages = [
            {
                "role": "system",
                "content": """Analyze price history and trends. Return JSON:
{
    "trend": "increasing|decreasing|stable",
    "confidence": 0.8,
    "prediction": "likely to increase/decrease in next 30 days",
    "best_time_to_buy": "now|wait|seasonal",
    "insights": "detailed analysis"
}"""
            },
            {
                "role": "user",
                "content": f"Price history: {json.dumps(price_history)}"
            }
        ]
        
        response = await self.call_llm(messages)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "trend": "stable",
                "confidence": 0.5,
                "prediction": "No clear prediction available",
                "best_time_to_buy": "now",
                "insights": "Insufficient data for analysis"
            }

# Global LLM service instance
llm_service = LLMService() 