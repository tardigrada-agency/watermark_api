FROM python:3.10.0rc1-slim-bullseye

RUN mkdir app

WORKDIR /app

COPY . .
RUN apt-get update
RUN apt-get -y --no-install-recommends install ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80

