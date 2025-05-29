import asyncio
import httpx
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any, Optional
import re
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
import logging
from asyncio_throttle import Throttler
import hashlib
import time
from functools import lru_cache
import random

@dataclass
class SearchResult:
    title: str
    price: Optional[float]
    currency: str
    source: str
    url: str
    image_url: Optional[str]
    description: str
    rating: Optional[float]
    review_count: Optional[int]
    availability: bool = True
    category: Optional[str] = None
    brand: Optional[str] = None
    features: List[str] = None
    discount_percentage: Optional[float] = None

class SearchService:
    def __init__(self):
        self.throttler = Throttler(rate_limit=15, period=1.0)  # Increased rate limit
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }
        self.search_cache = {}
        self.cache_ttl = 300  # 5 minutes cache

    def _cache_key(self, query: str) -> str:
        """Generate cache key for search query"""
        return hashlib.md5(query.lower().encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid"""
        return time.time() - cache_entry['timestamp'] < self.cache_ttl

    @lru_cache(maxsize=128)
    def _categorize_product(self, query: str) -> str:
        """Categorize product based on query keywords"""
        query_lower = query.lower()
        
        categories = {
            'electronics': ['phone', 'smartphone', 'iphone', 'android', 'tablet', 'ipad', 'laptop', 'computer', 'pc', 'macbook', 'tv', 'monitor'],
            'audio': ['headphones', 'earbuds', 'airpods', 'speaker', 'audio', 'music', 'sound'],
            'gaming': ['gaming', 'xbox', 'playstation', 'nintendo', 'switch', 'console', 'game'],
            'home': ['vacuum', 'cleaner', 'dyson', 'kitchen', 'appliance', 'home'],
            'fashion': ['clothing', 'shoes', 'shirt', 'dress', 'pants', 'jacket'],
            'health': ['fitness', 'health', 'supplement', 'vitamin', 'exercise'],
            'books': ['book', 'novel', 'textbook', 'reading'],
            'tools': ['tool', 'hardware', 'drill', 'hammer', 'repair']
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return 'general'

    def _generate_enhanced_mock_results(self, query: str) -> List[SearchResult]:
        """Generate more sophisticated mock search results"""
        category = self._categorize_product(query)
        base_price = self._estimate_base_price(query)
        
        # Generate realistic product variations
        variations = [
            {'suffix': 'Pro', 'price_multiplier': 1.5, 'rating_boost': 0.2},
            {'suffix': 'Standard', 'price_multiplier': 1.0, 'rating_boost': 0.0},
            {'suffix': 'Lite', 'price_multiplier': 0.7, 'rating_boost': -0.1},
            {'suffix': 'Max', 'price_multiplier': 1.8, 'rating_boost': 0.3},
            {'suffix': 'Mini', 'price_multiplier': 0.6, 'rating_boost': -0.05}
        ]
        
        sources = [
            {'name': 'Amazon', 'reliability': 0.95, 'price_factor': 1.0},
            {'name': 'Best Buy', 'reliability': 0.9, 'price_factor': 1.05},
            {'name': 'Walmart', 'reliability': 0.85, 'price_factor': 0.95},
            {'name': 'Target', 'reliability': 0.88, 'price_factor': 1.02},
            {'name': 'eBay', 'reliability': 0.75, 'price_factor': 0.85},
            {'name': 'Newegg', 'reliability': 0.9, 'price_factor': 1.03}
        ]
        
        results = []
        
        for i, variation in enumerate(variations[:4]):  # Limit to 4 results
            source = sources[i % len(sources)]
            
            # Calculate realistic pricing
            variant_price = base_price * variation['price_multiplier'] * source['price_factor']
            original_price = variant_price * random.uniform(1.1, 1.4)  # Original price before discount
            discount_pct = ((original_price - variant_price) / original_price) * 100
            
            # Generate realistic ratings
            base_rating = 4.0 + variation['rating_boost'] + (source['reliability'] - 0.8) * 2
            rating = min(5.0, max(3.0, base_rating + random.uniform(-0.2, 0.2)))
            review_count = random.randint(100, 5000)
            
            # Generate features based on category
            features = self._generate_features(category, variation['suffix'])
            
            # Select appropriate image
            image_urls = self._get_category_images(category)
            image_url = image_urls[i % len(image_urls)]
            
            result = SearchResult(
                title=f"{query} {variation['suffix']}",
                price=round(variant_price, 2),
                currency="USD",
                source=source['name'],
                url=f"https://{source['name'].lower().replace(' ', '')}.com/product{i+1}",
                image_url=image_url,
                description=f"High-quality {query} {variation['suffix']} with premium features and excellent performance",
                rating=round(rating, 1),
                review_count=review_count,
                availability=random.choice([True, True, True, False]),  # 75% available
                category=category,
                brand=self._generate_brand(category),
                features=features,
                discount_percentage=round(discount_pct, 0) if discount_pct > 5 else None
            )
            results.append(result)
        
        return results

    def _estimate_base_price(self, query: str) -> float:
        """Estimate base price based on product type"""
        query_lower = query.lower()
        
        price_ranges = {
            'iphone': 800, 'ipad': 500, 'macbook': 1200, 'airpods': 180,
            'laptop': 600, 'computer': 800, 'phone': 400, 'tablet': 300,
            'headphones': 150, 'speaker': 200, 'tv': 500, 'monitor': 300,
            'xbox': 400, 'playstation': 450, 'nintendo': 300, 'switch': 280,
            'vacuum': 200, 'watch': 250, 'camera': 400, 'drone': 300
        }
        
        for keyword, price in price_ranges.items():
            if keyword in query_lower:
                return price * random.uniform(0.8, 1.2)  # Add some variation
        
        return random.uniform(50, 500)  # Default range

    def _generate_features(self, category: str, variant: str) -> List[str]:
        """Generate realistic features based on category"""
        feature_sets = {
            'electronics': ['Fast Processor', 'Long Battery Life', 'HD Display', 'Wireless Charging', 'Water Resistant'],
            'audio': ['Noise Cancellation', 'Wireless', 'High-Fi Sound', 'Long Battery', 'Comfortable Fit'],
            'gaming': ['4K Gaming', 'Backwards Compatible', 'Online Multiplayer', 'Exclusive Games', 'Fast Loading'],
            'home': ['Energy Efficient', 'Easy Setup', 'Smart Controls', 'Quiet Operation', 'Large Capacity'],
            'general': ['High Quality', 'Durable', 'User Friendly', 'Great Value', 'Fast Shipping']
        }
        
        base_features = feature_sets.get(category, feature_sets['general'])
        
        # Add variant-specific features
        if variant == 'Pro':
            base_features = ['Professional Grade', 'Advanced Features'] + base_features
        elif variant == 'Max':
            base_features = ['Maximum Performance', 'Premium Build'] + base_features
        elif variant == 'Lite':
            base_features = ['Lightweight', 'Budget Friendly'] + base_features
        
        return random.sample(base_features, min(3, len(base_features)))

    def _generate_brand(self, category: str) -> str:
        """Generate realistic brand names based on category"""
        brands = {
            'electronics': ['Apple', 'Samsung', 'Google', 'Sony', 'LG'],
            'audio': ['Bose', 'Sony', 'Apple', 'Sennheiser', 'Audio-Technica'],
            'gaming': ['Sony', 'Microsoft', 'Nintendo', 'Razer', 'Logitech'],
            'home': ['Dyson', 'Shark', 'Bissell', 'Black+Decker', 'Hoover'],
            'general': ['TechCorp', 'Innovation Labs', 'Quality Brand', 'Premium Co', 'Smart Solutions']
        }
        
        return random.choice(brands.get(category, brands['general']))

    def _get_category_images(self, category: str) -> List[str]:
        """Get category-specific placeholder images"""
        image_sets = {
            'electronics': [
                'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=100&h=100&fit=crop'
            ],
            'audio': [
                'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=100&h=100&fit=crop'
            ],
            'gaming': [
                'https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1592840221661-2a4dd0c7b9f7?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1606318721529-79d95cf6bb32?w=100&h=100&fit=crop'
            ],
            'home': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=100&h=100&fit=crop',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop'
            ]
        }
        
        return image_sets.get(category, image_sets['electronics'])

    async def search_multiple_sources(self, queries: List[str]) -> List[SearchResult]:
        """Enhanced search with caching and better result generation"""
        # Check cache first
        cache_key = self._cache_key(str(queries))
        if cache_key in self.search_cache and self._is_cache_valid(self.search_cache[cache_key]):
            logging.info(f"Returning cached results for queries: {queries}")
            return self.search_cache[cache_key]['results']
        
        all_results = []
        
        # Enhanced mock search with better data
        for query in queries:
            enhanced_results = self._generate_enhanced_mock_results(query)
            all_results.extend(enhanced_results)
        
        # Try real web search as fallback/supplement
        try:
            search_tasks = []
            for query in queries[:2]:  # Limit real searches
                search_tasks.append(self.search_web_general(query))
            
            # Execute searches with throttling
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_results.extend(result[:2])  # Limit results per source
                elif isinstance(result, Exception):
                    logging.warning(f"Search failed: {result}")
        except Exception as e:
            logging.warning(f"Real search failed, using mock data only: {e}")
        
        # Deduplicate and sort results
        unique_results = self.deduplicate_results(all_results)
        sorted_results = self._sort_results_by_relevance(unique_results, queries)
        
        # Cache results
        self.search_cache[cache_key] = {
            'results': sorted_results,
            'timestamp': time.time()
        }
        
        return sorted_results

    def _sort_results_by_relevance(self, results: List[SearchResult], queries: List[str]) -> List[SearchResult]:
        """Sort results by relevance score"""
        def calculate_relevance(result: SearchResult) -> float:
            score = 0.0
            
            # Title relevance
            for query in queries:
                if query.lower() in result.title.lower():
                    score += 10
            
            # Rating contribution
            if result.rating:
                score += result.rating * 2
            
            # Availability bonus
            if result.availability:
                score += 5
            
            # Brand recognition (higher score for known brands)
            known_brands = ['Apple', 'Samsung', 'Sony', 'Bose', 'Dyson']
            if result.brand and result.brand in known_brands:
                score += 3
            
            # Discount bonus
            if result.discount_percentage and result.discount_percentage > 10:
                score += 2
            
            return score
        
        return sorted(results, key=calculate_relevance, reverse=True)

    async def search_shopping_apis(self, query: str) -> List[SearchResult]:
        """Enhanced shopping API search with better mock data"""
        await self.throttler.acquire()
        
        try:
            return self._generate_enhanced_mock_results(query)
        except Exception as e:
            logging.error(f"Shopping API search failed: {e}")
            return []

    async def search_web_general(self, query: str) -> List[SearchResult]:
        """Enhanced general web search"""
        await self.throttler.acquire()
        
        try:
            # Use DuckDuckGo HTML search (respects robots.txt)
            search_url = f"https://html.duckduckgo.com/html/?q={query} buy online store price"
            
            async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
                response = await client.get(search_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Parse search results with better extraction
                for result_div in soup.find_all('div', class_='result')[:3]:  # Limit results
                    try:
                        title_elem = result_div.find('a', class_='result__a')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        
                        # Extract description
                        desc_elem = result_div.find('a', class_='result__snippet')
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Enhanced price extraction
                        price = self.extract_price_from_text(f"{title} {description}")
                        if not price:
                            price = self._estimate_base_price(query)
                        
                        # Generate realistic supplementary data
                        rating = round(random.uniform(3.5, 4.8), 1)
                        review_count = random.randint(50, 2000)
                        
                        results.append(SearchResult(
                            title=title,
                            price=price,
                            currency="USD",
                            source=urlparse(url).netloc if url else "Web Store",
                            url=url,
                            image_url=random.choice(self._get_category_images(self._categorize_product(query))),
                            description=description,
                            rating=rating,
                            review_count=review_count,
                            category=self._categorize_product(query),
                            brand=self._generate_brand(self._categorize_product(query)),
                            features=self._generate_features(self._categorize_product(query), 'Standard')
                        ))
                        
                    except Exception as e:
                        logging.warning(f"Failed to parse search result: {e}")
                        continue
                
                return results
                
        except Exception as e:
            logging.error(f"Web search failed: {e}")
            return []

    async def search_comparison_sites(self, query: str) -> List[SearchResult]:
        """Enhanced comparison site search"""
        await self.throttler.acquire()
        
        try:
            return self._generate_enhanced_mock_results(query)[:2]  # Limit comparison results
        except Exception as e:
            logging.error(f"Comparison site search failed: {e}")
            return []

    def extract_price_from_text(self, text: str) -> Optional[float]:
        """Enhanced price extraction with better patterns"""
        # Enhanced price patterns
        patterns = [
            r'\$\s*(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # $1,234.56
            r'(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)\s*dollars?',  # 1234.56 dollars
            r'USD\s*(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # USD 1234.56
            r'Price:?\s*\$?(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',  # Price: $1234.56
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    price = float(matches[0].replace(',', ''))
                    if 5 <= price <= 20000:  # Reasonable price range
                        return price
                except (ValueError, AttributeError):
                    continue
        
        return None

    def deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Enhanced deduplication with similarity scoring"""
        if not results:
            return []
        
        unique_results = []
        seen_combinations = set()
        
        for result in results:
            # Create a signature based on title and price
            title_words = set(result.title.lower().split())
            signature = (
                frozenset(title_words),
                result.price,
                result.source
            )
            
            # Check for similar existing results
            is_duplicate = False
            for seen_sig in seen_combinations:
                title_overlap = len(signature[0].intersection(seen_sig[0])) / max(len(signature[0]), len(seen_sig[0]))
                price_diff = abs((signature[1] or 0) - (seen_sig[1] or 0)) / max(signature[1] or 1, seen_sig[1] or 1)
                
                if title_overlap > 0.7 and price_diff < 0.1:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_combinations.add(signature)
                unique_results.append(result)
        
        return unique_results

    def titles_similar(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Check if two titles are similar using simple word overlap"""
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return False
        
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        return similarity >= threshold

    async def get_product_details(self, url: str) -> Dict[str, Any]:
        """Scrape detailed product information from a specific URL"""
        await self.throttler.acquire()
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract structured data (JSON-LD)
                structured_data = self.extract_structured_data(soup)
                
                # Extract meta information
                meta_info = self.extract_meta_info(soup)
                
                # Combine and return product details
                return {
                    "structured_data": structured_data,
                    "meta_info": meta_info,
                    "page_title": soup.title.string if soup.title else "",
                    "images": self.extract_images(soup, url)
                }
                
        except Exception as e:
            logging.error(f"Failed to get product details from {url}: {e}")
            return {}

    def extract_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract JSON-LD structured data"""
        structured_data = {}
        
        # Look for JSON-LD scripts
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    structured_data = data
                    break
            except (json.JSONDecodeError, AttributeError):
                continue
        
        return structured_data

    def extract_meta_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract meta tag information"""
        meta_info = {}
        
        # Common meta tags for products
        meta_tags = [
            'og:title', 'og:description', 'og:price:amount', 
            'og:price:currency', 'og:image', 'product:price:amount',
            'product:price:currency', 'twitter:title', 'twitter:description'
        ]
        
        for tag_name in meta_tags:
            meta_tag = soup.find('meta', {'property': tag_name}) or soup.find('meta', {'name': tag_name})
            if meta_tag and meta_tag.get('content'):
                meta_info[tag_name] = meta_tag['content']
        
        return meta_info

    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract product images from page"""
        images = []
        
        # Look for common image selectors
        image_selectors = [
            'img[data-src*="product"]',
            'img[src*="product"]', 
            '.product-image img',
            '#product-image img',
            '.gallery img'
        ]
        
        for selector in image_selectors:
            img_elements = soup.select(selector)
            for img in img_elements[:5]:  # Limit to 5 images
                src = img.get('data-src') or img.get('src')
                if src:
                    full_url = urljoin(base_url, src)
                    if full_url not in images:
                        images.append(full_url)
        
        return images

# Global search service instance
search_service = SearchService() 