# syntax = edrevo/dockerfile-plus

INCLUDE+ Dockerfile

COPY requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

ENV PYTHONPATH $PYTHONPATH:/home/app
