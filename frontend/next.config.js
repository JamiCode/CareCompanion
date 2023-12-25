/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    this.compiler = {
      removeConsole: process.env.NODE_ENV === "production",
    };
    console.log("h", process.env.API_URL);
    const chech =
      process.env.NODE_ENV === "development"
        ? process.env.API_URL_DEV
        : process.env.API_URL_PROD;

    console.log("chech", chech);
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
