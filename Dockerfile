FROM python:3.13-slim

COPY /src /mnt/src
COPY /tests /mnt/tests
COPY /requirements.txt /mnt/requirements.txt

RUN pip install --no-cache-dir -r /mnt/requirements.txt

CMD ["python", "/mnt/src/main.py"]
