FROM nginx:1.21.5-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY robots.txt /app/robots.txt