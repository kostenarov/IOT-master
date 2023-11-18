FROM python AS server-image

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --target=/app/dependencies

FROM alpine AS runtime-image

RUN apk --no-cache add python3

COPY --from=server-image /app/dependencies /usr/lib/python3.11/site-packages

COPY . /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT python3 flask_app.py