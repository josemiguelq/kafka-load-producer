from kafka import KafkaProducer
from time import sleep
import os
import json
import uuid


class KafkaMock:
    def start_producer(self):
        producer = KafkaProducer(bootstrap_servers=BROKER, request_timeout_ms=int(os.getenv('KAFKA_REQUEST_TIMEOUT_MS'))
                                 , value_serializer=lambda x: json.dumps(x).encode(DEFAULT_ENCODING))
        i = 0
        for i in range(int(NUMBER_OF_REQUESTS)):
            print("Enviando requisição " + str(i + 1) + " de " + NUMBER_OF_REQUESTS)
            for line in open("payload.txt", "r"):
                header = self.get_default_headers()
                body = self.include_body_attribute_on_payload(line)
                print("[headers]: " + str(header))
                print("[body]: " + str(body))
                producer.send(TOPIC, value=body,
                              headers=header)
                sleep(float(INTERVAL))
            print("")

    @staticmethod
    def include_body_attribute_on_payload(payload):
        return {
            'body': json.loads(s=payload)
        }

    @staticmethod
    def get_default_headers():
        s_uuid = str(uuid.uuid4())
        return [
            ('contentType', b'application/json'),
            ('correlationId', str(uuid.uuid4()).encode())
        ]


if __name__ == '__main__':
    NUMBER_OF_REQUESTS = os.getenv("NUMBER_OF_REQUESTS")
    INTERVAL = os.getenv("INTERVAL")
    BROKER = os.getenv("BROKER")
    TOPIC = os.getenv("TOPIC")
    DEFAULT_ENCODING = 'utf-8'
    KafkaMock().start_producer()