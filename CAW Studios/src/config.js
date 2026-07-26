const { z } = require("zod");
// FIX 1: By default, dotenv.config() does NOT override existing process.env.
// This ensures system environment variables (Docker/CI) win over .env file.
require("dotenv").config(); 

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "staging", "production"]),
  PORT: z.coerce.number().int().positive(),
  // FIX 3: Remove the 'localhost' default. If missing, it MUST crash.
  DATABASE_URL: z.string().url(),
  // FIX 2: Ensure JWT_SECRET is explicitly required and validated.
  JWT_SECRET: z.string().min(32),
  CORS_ORIGIN: z.string().url(),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error("CRITICAL: Invalid environment configuration:");
  console.error(parsed.error.format());
  process.exit(1);
}

module.exports = parsed.data;
