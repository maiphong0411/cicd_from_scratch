FROM python:3.13-alpine
WORKDIR /app
COPY app/app.py .
ENV PYTHONUNBUFFERED=1
USER nobody
EXPOSE 8000
CMD ["python", "app.py"]
