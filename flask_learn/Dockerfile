FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# environment variables
ENV DEBUG=false
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY flask_learn/requirements.txt .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "flask_learn.main:app"]
