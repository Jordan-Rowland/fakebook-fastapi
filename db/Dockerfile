# pull official base image
FROM mysql:latest

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
