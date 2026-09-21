FROM --platform=linux/amd64 nginx:alpine

LABEL Name="Anttu's homepage" Version="3.0"

COPY index.html /usr/share/nginx/html/index.html
COPY static/ /usr/share/nginx/html/static/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
