FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "/aiogram_run.py"]