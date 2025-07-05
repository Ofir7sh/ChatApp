FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

COPY init_db/wait-for-it.sh ./init_db/wait-for-it.sh
RUN chmod +x ./init_db/wait-for-it.sh

CMD ["./init_db/wait-for-it.sh", "db:1433", "-t", "45", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
