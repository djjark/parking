# Build Stage
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy package files first (improves Docker caching)
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy all project files
COPY . .

# Build Vite project
RUN npm run build

# Production Stage
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default Nginx files
RUN rm -rf ./*

# Copy built frontend assets from the build stage
COPY --from=build /app/dist . 

# Copy custom Nginx configuration
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose the correct port
EXPOSE 81

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
