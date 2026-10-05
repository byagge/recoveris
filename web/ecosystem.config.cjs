/** PM2 config — isolated process for recoveris.arix.vu only */
module.exports = {
  apps: [
    {
      name: "recoveris",
      cwd: __dirname,
      script: "node_modules/next/dist/bin/next",
      args: "start -p 3011 -H 127.0.0.1",
      env: {
        NODE_ENV: "production",
        PORT: "3011",
        HOSTNAME: "127.0.0.1",
      },
      instances: 1,
      autorestart: true,
      max_memory_restart: "512M",
    },
  ],
};
