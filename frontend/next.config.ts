import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/agents/:path*',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://localhost:8000/agents/:path*' 
          : '/agents/:path*',
      },
      {
        source: '/brands',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://localhost:8000/brands' 
          : '/brands',
      },
    ];
  },
};

export default nextConfig;
