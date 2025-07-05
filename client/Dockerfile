FROM python:3.12-slim

WORKDIR /app

COPY client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY client/ ./
RUN mkdir -p ./app/core
COPY app/core/config.py ./app/core/config.py
 

ENV PYTHONPATH=/app

CMD ["python", "cli.py"]
