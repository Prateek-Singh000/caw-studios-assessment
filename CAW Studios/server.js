const config = require("./src/config.js");

console.log(
  JSON.stringify({
    message: "Service starting",
    environment: config.NODE_ENV,
    port: config.PORT,
    log_level: config.LOG_LEVEL,
    // NOTE: We DO NOT log DATABASE_URL or JWT_SECRET
  })
);

// Simulate app starting
console.log(`Server listening on port ${config.PORT}`);
