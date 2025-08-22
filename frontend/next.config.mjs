/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['drizzle-orm']
  },
  async rewrites() {
    return [
      {
        source: '/api/tutor/:path*',
        destination: `${process.env.BACKEND_API_URL || 'http://localhost:8000'}/api/:path*`
      }
    ]
  }
}

export default nextConfig