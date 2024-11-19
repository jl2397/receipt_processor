# Receipt Processor

This receipt processor is written in Python 3.12 using the FastAPI framework. To run the dockerized application, clone the repository onto your local machine and navigate to the `receipt_processor` directory. This contains the Dockerfile for the application, from which you can run the following commands: 

```docker build -t receipt-processor .```

```docker run -it -d -p 80:80 receipt-processor```

The application should now be running on port 80. You can confirm this by accessing the health endpoint here: `http://0.0.0.0:80/health`. Now you should be able to post a receipt at `http://0.0.0.0:80/receipts/process` and retrieve its associated points at `http://0.0.0.0:80/receipts/{id}/points`.

An outline of the OpenAPI specs for this application can be found here, `http://0.0.0.0:80/docs`, with the expected receipt request schemas listed under the `Receipt` section.