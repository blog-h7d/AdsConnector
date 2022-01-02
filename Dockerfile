FROM python:3.10-slim-buster
WORKDIR /code

RUN apt-get update && apt-get install make

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY adslib/adslib.so /usr/lib/adslib.so
RUN chmod 755 /usr/lib/adslib.so

RUN apt-get remove make -y && apt autoremove && apt clean

COPY / /code/
CMD ["python", "controller.py", "-p", "8002"]