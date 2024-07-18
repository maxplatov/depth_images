FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /home/app/
COPY . .

ENV PYTHONPATH $PYTHONPATH:/home/app

CMD ["python", "run.py"]
