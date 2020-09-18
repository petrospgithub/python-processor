import os
import pika
import sys
import logging as logger
from util.http_status_server import HttpHealthServer
from util.task_args import get_input_channel, get_output_channel, get_name, get_reverse_string

logger.basicConfig(level=logger.INFO)
HttpHealthServer.run_thread()

host = os.environ['SPRING_RABBITMQ_HOST']
port = int(os.environ['SPRING_RABBITMQ_PORT'])

logger.info("intput: {}".format(get_input_channel()))
logger.info("output: {}".format(get_output_channel()))
logger.info("name: {}".format(get_name()))

input = "{0}.{1}".format(get_input_channel(), get_name())
output = "{0}.{1}".format(get_output_channel(), get_name())

# Consumer
consumer = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
channel_consumer = consumer.channel()
channel_consumer.queue_declare(queue=input, durable=True)
# Consumer

# Producer
producer = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
channel_producer = producer.channel()
channel_producer.queue_declare(queue=output, durable=True)
# Producer


def on_message(ch, method, properties, body):
    # print(method_frame.delivery_tag)
    logger.info(" [x] Received %r" % body)
    channel_producer.basic_publish(exchange='',
                                   routing_key=output,
                                   body=get_reverse_string(body))


channel_consumer.basic_consume(queue=input,
                               auto_ack=True,
                               on_message_callback=on_message)
try:
    channel_consumer.start_consuming()
except KeyboardInterrupt:
    raise
# channel.stop_consuming()
# connection.close()
