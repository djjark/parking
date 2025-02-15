# Use the official Nginx image as the base image
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /etc/nginx

# Copy the custom Nginx configuration file to the container
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (inside container) that Nginx will listen on
EXPOSE 80

# Copy the frontend build files from the build stage to Nginx's default directory
# Adjust the path to your build directory if necessary
COPY ../frontend/dist /usr/share/nginx/html

# Start Nginx in the foreground (daemon off)
CMD ["nginx", "-g", "daemon off;"]
