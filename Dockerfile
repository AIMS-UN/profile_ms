FROM python:3.7-alpine

ADD . /app
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

COPY . .

CMD python src/app.py