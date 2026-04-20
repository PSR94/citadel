import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@citadel/shared-types", "@citadel/ui", "@citadel/config"],
};

export default nextConfig;
