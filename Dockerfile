FROM python:3.10-slim-buster
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY / /code/
CMD ["python", "controller.py"]