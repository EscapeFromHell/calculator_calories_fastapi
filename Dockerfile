FROM python:3.10

RUN mkdir /app

COPY app/ /app

WORKDIR /app

ENV PYTHONPATH=/app

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install

CMD ["./run.sh"]
