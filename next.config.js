/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: [
      'example.com', 
      'amazon.com', 
      'ebay.com', 
      'bestbuy.com', 
      'walmart.com', 
      'target.com',
      'images.unsplash.com',
      'via.placeholder.com',
      'picsum.photos'
    ],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig 