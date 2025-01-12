# Stage 1: Build the React app
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the source code
COPY . .

# Build the React app
RUN npm run build  # This creates the build directory

# Stage 2: Serve the React app with Nginx
FROM nginx:alpine

# Copy the build output from the 'build' stage to the Nginx web directory
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
# Copy the custom Nginx config
RUN ls
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
