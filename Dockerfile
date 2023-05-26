FROM python:3.10-alpine3.17
WORKDIR /opt/hyperday
COPY requirements.txt .
RUN apk add --no-cache gcc libcurl libc-dev pkgconfig linux-headers zeromq-dev python3-dev && rm -rf /var/cache/apk/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=src:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
CMD ["python3", "-m", "flask", "run"]