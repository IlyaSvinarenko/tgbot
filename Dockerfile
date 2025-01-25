FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 -r requirements.txt

COPY * /app/

ENTRYPOINT ["python", "/app/aiogram_run.py"]