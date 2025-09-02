FROM python:3.12

WORKDIR /home/myapp

COPY . /home/myapp
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u","worker.py"]