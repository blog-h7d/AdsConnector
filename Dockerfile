FROM python:3.10-slim-buster
WORKDIR /code

RUN apt-get update && apt-get install make

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN cd adslib && make && make install

RUN apt-get remove make -y && apt autoremove && apt clean

COPY / /code/
CMD ["python", "controller.py"]