FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

RUN addgroup --system northwind \
    && adduser --system --ingroup northwind northwind

COPY app ./app
COPY run.py ./run.py

RUN chown -R northwind:northwind /app

USER 100:101

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["python", "-m", "app"]