FROM python:3.9.16-slim-buster

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY src /src

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]