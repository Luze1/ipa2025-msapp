FROM python
RUN pip3 install flask pymongo bson
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  app.py /home/myapp/
EXPOSE 8080
CMD python3 /home/myapp/app.py
