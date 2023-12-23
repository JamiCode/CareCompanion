/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const destinationUrl = process.env.API_URL;

    return [
      {
        source: "/api/:path*",
        destination: `${destinationUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
