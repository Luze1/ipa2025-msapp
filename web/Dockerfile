FROM python

WORKDIR /home/myapp

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY ./static ./static
COPY ./templates ./templates
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]