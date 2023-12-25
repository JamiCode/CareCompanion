/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    API_KEY: process.env.API_KEY,
    API_URL: process.env.API_URL_PROD,
  },

  async rewrites() {
    this.compiler = {
      removeConsole: process.env.NODE_ENV === "production",
    };

    const destinationUrl =
      process.env.NODE_ENV === "development"
        ? process.env.API_URL_DEV
        : process.env.API_URL_PROD;

    return [
      {
        source: "/api/:path*",
        destination: `${destinationUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
