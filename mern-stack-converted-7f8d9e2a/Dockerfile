# Stage 1: Python backend
FROM python:3.9-slim AS backend

WORKDIR /app

COPY python-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python-backend .

EXPOSE 5001

# Stage 2: Nginx for frontend and reverse proxy
FROM nginx:alpine

# Copy the built React app
COPY react-frontend/source /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy backend from previous stage
COPY --from=backend /app /app

# Install Python and dependencies in Nginx image
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir -r /app/requirements.txt

# Expose port 80
EXPOSE 80

# Start Nginx and Python app
CMD nginx && python3 /app/main.py