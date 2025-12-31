/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', 's3.amazonaws.com'],
  },
  // Experimental features
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
