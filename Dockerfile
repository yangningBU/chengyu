# Build stage: fingerprint assets with a content hash so browsers fetch new
# versions immediately while unchanged files stay cached.
FROM alpine:3.20 AS build
WORKDIR /site
COPY index.html style.css app.js chengyu.csv ./

# Rename each asset to name.<hash>.ext and rewrite references to it. Order
# matters: chengyu.csv is referenced by app.js, so it must be hashed first.
RUN set -eu; \
    fingerprint() { \
      file="$1"; shift; \
      hash=$(sha256sum "$file" | cut -c1-8); \
      new="${file%.*}.$hash.${file##*.}"; \
      mv "$file" "$new"; \
      for ref in "$@"; do sed -i "s|\"$file\"|\"$new\"|g" "$ref"; done; \
    }; \
    fingerprint chengyu.csv app.js; \
    fingerprint app.js index.html; \
    fingerprint style.css index.html; \
    ls -1

# Dev stage: serves the mounted source files with live reload (CSS is
# hot-swapped, other changes reload the page). See compose.yaml.
FROM node:22-alpine AS dev
RUN npm install -g browser-sync@3
WORKDIR /site
EXPOSE 3000
CMD ["browser-sync", "start", "--server", "--files", "index.html,style.css,app.js,chengyu.csv", \
     "--port", "3000", "--no-open", "--no-notify", "--no-ui"]

# Static site served by nginx. Railway injects $PORT at runtime.
FROM nginx:1.27-alpine

ENV PORT=8080

# The nginx image runs envsubst on /etc/nginx/templates/*.template at startup.
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /site/ /usr/share/nginx/html/

EXPOSE 8080
