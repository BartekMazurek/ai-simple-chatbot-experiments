FROM python:3.10-slim

RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir sentence-transformers

COPY ./docker/model/get_model.py /app/get_model.py
WORKDIR /app

CMD ["python", "get_model.py"]
