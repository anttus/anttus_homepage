FROM nginx:alpine-slim

LABEL Name="Anttu's homepage" Version="3.0"

COPY index.html /usr/share/nginx/html/index.html
COPY static/ /usr/share/nginx/html/static/

EXPOSE 5050

CMD ["nginx", "-g", "daemon off;"]
