FROM nginx:alpine

ARG GIST_ID=d1285d208ef1cb4d54e27561251e38cd

LABEL org.opencontainers.image.authors="Anttu Suhonen" \
	org.opencontainers.image.description="Anttu's homepage" \
	org.opencontainers.image.version="3.0.0"

COPY index.html /usr/share/nginx/html/index.html
COPY static/ /usr/share/nginx/html/static/
RUN curl -sSL "https://gist.githubusercontent.com/raw/${GIST_ID}" > /usr/share/nginx/html/static/cv-data.json

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
