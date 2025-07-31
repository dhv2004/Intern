
FROM python:3.11

WORKDIR /app


COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt


COPY . .


ENV PYTHONPATH=/app


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

