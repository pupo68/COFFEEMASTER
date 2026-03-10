FROM nginx:alpine

# Copiar os arquivos estáticos para o diretório padrão do Nginx
COPY . /usr/share/nginx/html

# Expor a porta 80 (padrão HTTP)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
