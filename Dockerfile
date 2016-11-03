FROM fedoraqa/flask-base:24

ADD ./docker_data/tflink-taskotron-fedora.repo /etc/yum.repos.d/
RUN dnf install -y resultsdb_api && dnf clean all
COPY . /usr/src/resultsdb_frontend
COPY ./docker_data/settings.py /usr/src/resultsdb_frontend/conf/
WORKDIR /usr/src/resultsdb_frontend
EXPOSE 5002
ENV DEV true
RUN pip install -r requirements.txt

CMD ["python", "runapp.py"]
