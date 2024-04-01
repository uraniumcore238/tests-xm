FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY xm /app/xm

CMD ["uvicorn", "xm.orders:app", "--host", "0.0.0.0"]