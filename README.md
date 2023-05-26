## Hypermon

### Deploy
```bash
docker build -t hypermon .
docker run -d --name hypermon -p 8080:8080 --env-file=./.env hypermon:latest
```

_.env_ - Содержит OS_USERNAME, OS_PASSWORD и т.д. (от admin)

Go to http://0.0.0.0:8080