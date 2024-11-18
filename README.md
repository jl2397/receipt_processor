# Receipt Processor

This receipt processor is written in Python 3.12 using the FastAPI framework. To run the dockerized application, navigate to the root directory of the `receipt_processor` directory, which contains the Dockerfile, and run the following commands: 

```docker build -t receipt-processor .```

```docker run -it -d -p 80:80 receipt-processor```

The application can now be accessed at `http://0.0.0.0:80/health` and the OpenAPI specs can be found at `http://0.0.0.0:80/docs`. Now you can post a receipt at `http://0.0.0.0:80/receipts/process` and get the associated points  at `http://0.0.0.0:80/receipts/{id}/points`.

The expected receipt request schemas are listed in the OpenAPI spec under `Receipt`.