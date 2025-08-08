FROM python:3.11-slim

RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir sentence-transformers

COPY ./docker/model1/get_model_1.py /app/get_model_1.py
WORKDIR /app

CMD ["python", "get_model_1.py"]
