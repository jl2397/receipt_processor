FROM python:3.12

WORKDIR /receipt-processor

COPY requirements.txt /receipt-processor/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /receipt-processor/requirements.txt

COPY . /receipt-processor


CMD ["fastapi", "run", "/receipt-processor/app.py", "--port", "80"]