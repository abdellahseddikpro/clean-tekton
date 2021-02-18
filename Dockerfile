FROM python:3.9.1-alpine
ENV PYTHONUNBUFFERED=0

WORKDIR /app
COPY clean.py ./

RUN pip install --no-cache-dir requests

CMD ["python", "clean.py"]
