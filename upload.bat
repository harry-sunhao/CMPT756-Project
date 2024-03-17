@echo off
echo Building Docker Image...
docker build -t flaskproject .
echo Tagging Docker Image...
docker tag flaskproject harry0807/flaskproject
echo Pushing Docker Image...
docker push harry0807/flaskproject
echo Done.
pause