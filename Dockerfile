FROM bitnami/pytorch:2.1.1

WORKDIR /app

COPY . /app

RUN pip install flask torch torchvision matplotlib

EXPOSE 5000

CMD ["python", "app.py"]
