/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const destinationUrl = "https://carecompanion-production.up.railway.app";
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
