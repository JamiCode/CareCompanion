/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const destinationUrl = process.env.API_URL;
    console.log("destinationUrl", destinationUrl);
    return [
      {
        source: "/api/:path*",
        destination: `${destinationUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
