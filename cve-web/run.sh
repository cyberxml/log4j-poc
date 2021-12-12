docker stop cve-web
docker rm cve-web
docker run -d -p 8080:8080 --name cve-web cve-web:1
