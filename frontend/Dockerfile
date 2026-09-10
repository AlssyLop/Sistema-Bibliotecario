# Build stage
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# React Router support: fallback to index.html
RUN echo 'server { \
    listen 8001; \
    charset utf-8; \
    location / { \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    try_files $uri $uri/ /index.html; \
    } \
    types { \
    text/html html htm; \
    text/css css; \
    application/javascript js; \
    application/json json; \
    } \
    }' > /etc/nginx/conf.d/default.conf

EXPOSE 8001
CMD ["nginx", "-g", "daemon off;"]
