# Static site served by nginx. Railway injects $PORT at runtime.
FROM nginx:1.27-alpine

ENV PORT=8080

# The nginx image runs envsubst on /etc/nginx/templates/*.template at startup.
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY index.html chengyu.csv /usr/share/nginx/html/

EXPOSE 8080
