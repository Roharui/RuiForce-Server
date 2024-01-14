from dotenv import load_dotenv
import os

import pika
import json

import random

load_dotenv()

ENV = {**os.environ}


class Consumer:
    def __init__(self):
        self.__url = ENV["MQ_HOST"]
        self.__port = int(ENV["MQ_PORT"])
        self.__vhost = "/"
        self.__cred = pika.PlainCredentials(ENV["MQ_ID"], ENV["MQ_PW"])
        self.__queue = ENV["MQ_QUEUE"]

    def on_message(channel, method_frame, header_frame, body):
        channel.basic_publish(
            "",
            routing_key=header_frame.reply_to,
            body=json.dumps({"angle": random.randint(-2, 2)}),
        )

    def main(self):
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.__url, self.__port, self.__vhost, self.__cred
            )
        )
        chan = conn.channel()
        chan.basic_consume(
            queue=self.__queue, on_message_callback=Consumer.on_message, auto_ack=True
        )

        print("Consumer is starting...")
        chan.start_consuming()


if __name__ == "__main__":
    try:
        consumer = Consumer()
        consumer.main()
    except KeyboardInterrupt:
        pass
