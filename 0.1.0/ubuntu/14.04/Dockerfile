FROM ubuntu:14.04

RUN apt-get update && apt-get install -y curl python python-pip && \
pip install jinja2 kazoo

COPY init.py haproxy.cfg.j2 /

CMD ["/init.py"]
