import pika


class BaseConsumer:
    def __init__(self, ENV):
        self.__url = ENV["MQ_HOST"]
        self.__port = int(ENV["MQ_PORT"])
        self.__vhost = "/"
        self.__cred = pika.PlainCredentials(ENV["MQ_ID"], ENV["MQ_PW"])
        self.__queue = ENV["MQ_QUEUE"]

    def on_message(channel, method_frame, header_frame, body):
        pass

    def main(self):
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                self.__url, self.__port, self.__vhost, self.__cred
            )
        )
        chan = conn.channel()
        chan.basic_consume(
            queue=self.__queue,
            on_message_callback=self.__class__.on_message,
            auto_ack=True,
        )

        print("Consumer is starting...")
        chan.start_consuming()
