# --- Frontend Dockerfile ---
# Stage 1: Build
FROM node:18-slim AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:stable-alpine

# Copy built assets from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config if needed, otherwise use default
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
