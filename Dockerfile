FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
RUN --mount=type=cache,target=/root/.cache/pip pip install .
RUN chmod +x ./setup.sh
RUN chmod +x ./dramatiq.sh