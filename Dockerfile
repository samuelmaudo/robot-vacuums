FROM python:3.9-slim as base

RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
USER app_user
COPY app ./app/
COPY main.py ./

FROM base as command

ENTRYPOINT ["python", "main.py"]
CMD ["5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM"]

FROM base as tests

COPY tests ./tests/
ENTRYPOINT ["pytest"]
CMD ["tests"]