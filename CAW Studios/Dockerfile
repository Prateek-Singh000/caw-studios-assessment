# --- Stage 1: Builder (The Prep Kitchen) ---
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
# Only install production dependencies
RUN npm install --omit=dev
# Copy source code
COPY . .

# --- Stage 2: Runtime (The Clean Plate) ---
FROM node:20-slim
WORKDIR /app

# Copy ONLY the artifacts we need from the builder, with correct ownership
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/package*.json ./
COPY --from=builder --chown=node:node /app/server.js ./

# Drop root privileges for security
USER node

EXPOSE 3000
CMD ["node", "server.js"]
