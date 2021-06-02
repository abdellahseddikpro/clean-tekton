FROM python:3.9.5-alpine
ENV PYTHONUNBUFFERED=0

WORKDIR /app
COPY garbage_collector.py ./

RUN pip install --no-cache-dir requests

CMD ["python", "garbage_collector.py"]
