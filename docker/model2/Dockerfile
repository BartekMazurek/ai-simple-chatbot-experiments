FROM python:3.11-slim

RUN pip install --no-cache-dir \
    transformers[torch] \
    sentencepiece \
    protobuf

COPY ./docker/model2/get_model_2.py /app/get_model_2.py
WORKDIR /app

CMD ["python", "get_model_2.py"]
