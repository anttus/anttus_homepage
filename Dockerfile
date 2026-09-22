FROM --platform=linux/amd64 nginx:alpine

ARG GIST_ID=d1285d208ef1cb4d54e27561251e38cd

LABEL Name="Anttu's homepage" Version="3.0"

COPY index.html /usr/share/nginx/html/index.html
COPY static/ /usr/share/nginx/html/static/

RUN curl -s "https://api.github.com/gists/${GIST_ID}" | grep -o '"content": ".*"' | head -n 1 | sed 's/"content": "//;s/"$//' > /usr/share/nginx/html/static//cv-data.json

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
