/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    this.compiler = {
      removeConsole: process.env.NODE_ENV === "production",
    };
    const destinationUrl =
      "https://carecompanion-production-a0ae.up.railway.app/";
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
