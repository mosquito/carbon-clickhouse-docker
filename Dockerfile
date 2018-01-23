FROM python:2-alpine

RUN pip install toml

ENV DOCKER_ENTRYPOINT /usr/bin/carbon-clickhouse

ADD carbon-clickhouse /usr/bin/carbon-clickhouse
ADD entrypoint.py /usr/bin/entrypoint
ADD config.base.toml /etc/config.base.toml

RUN chmod a+x /usr/bin/carbon-clickhouse /usr/bin/entrypoint

ENTRYPOINT ["/usr/bin/entrypoint"]
