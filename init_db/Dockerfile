FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN chmod +x init_db/wait-for-it.sh

CMD ["./init_db/wait-for-it.sh", "db:1433", "--", "python", "init_db/init_db.py"]
