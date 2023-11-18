FROM python AS car-image

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --target=/app/dependencies

FROM alpine AS runtime-image

RUN apk --no-cache add python3

COPY --from=car-image /app/dependencies /usr/lib/python3.11/site-packages

COPY . /app

WORKDIR /app

ENTRYPOINT python3 car_handler.py