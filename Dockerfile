FROM python:3.10.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]