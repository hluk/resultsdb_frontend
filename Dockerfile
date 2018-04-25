FROM fedoraqa/flask-base:24

RUN dnf install -y python-resultsdb_api && dnf clean all
COPY . /usr/src/resultsdb_frontend
COPY ./docker_data/settings.py /usr/src/resultsdb_frontend/conf/
WORKDIR /usr/src/resultsdb_frontend
EXPOSE 5002
ENV DEV true
RUN pip install -r requirements.txt

CMD ["python", "runapp.py"]
