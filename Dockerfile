FROM python:3.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /code/logs
RUN chmod 777 /code/logs
WORKDIR /code
COPY . /code
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
RUN apt-get install libfontconfig
RUN apt-get update
RUN apt-get -y install vim



ENV C_QUEUE to_create
ENV A_QUEUE to_analysis
ENV S_QUEUE to_save
ENV QUEUE to_create

CMD /code/docker-entrypoint.sh
#ENTRYPOINT ["celery", "-A", "handle_data", "worker", "-l", "info", "-Q"]
