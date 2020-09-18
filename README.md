# python-processor

The example code in this section shows how to run a Python script
as a processor within a Data Flow Stream.
In this guide, we package the Python script as a Docker image and
deploy it to Kubernetes. We use RabbitMQ as the messaging middleware.


The guide demonstrates time series streaming data pipeline.
It receives data stream over scdf-rabbitmq-source/

The processor uses the pika library to create
consumer and producer connections.

The main loop of execution resides in python_processor.py.
