FROM ubuntu:18.04

EXPOSE 8888

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "python3"]

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "python3-pip"]
RUN ["pip3", "install", "--upgrade", "pip"]
RUN ["pip", "install", "jupyter"]


RUN ["mkdir", "/notebooks"]

COPY ./jupyter_notebook_config.py /
COPY ./start.sh /
ENTRYPOINT ["/start.sh"]

# docker build -t fts_notebook .
# docker run --rm -it -p 8888:8888 -p 5900:5900 --mount type=bind,src=/Users/sergey/PycharmProjects/full-text-search/notebooks,dst=/notebooks fts_notebook
#    oder
# docker create --name my_notebook_p3 --mount type=bind,src=/Users/sergey/PycharmProjects/full-text-search/notebooks,dst=/notebooks -p 8888:8888 fts_notebook
# docker start fts_notebook
