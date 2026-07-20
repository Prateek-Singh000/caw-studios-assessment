const { z } = require("zod");

const schema = z.object({
  NODE_ENV: z.enum(["development", "production"]),
  DB_URL: z.string().url(),
}).refine(
  (data) => !(data.NODE_ENV === "production" && data.DB_URL.includes("localhost")),
  { message: "CRITICAL: Production DB_URL cannot be localhost!" }
);

const parsed = schema.safeParse({
  NODE_ENV: process.env.NODE_ENV || "development",
  DB_URL: process.env.DB_URL || "postgres://localhost:5432/default",
});

if (!parsed.success) {
  console.error("Configuration validation failed:");
  console.error(parsed.error.format());
  process.exit(1);
}

console.log("Service starting successfully in environment:", parsed.data.NODE_ENV);
