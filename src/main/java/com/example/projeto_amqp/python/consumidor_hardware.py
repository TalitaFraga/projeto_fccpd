import pika
import csv
import time

def callback(ch, method, properties, body):
    mensagem = body.decode()
    print(f"Novo chamado de Hardware - {mensagem}")

    # Gravar no arquivo auditoria_hardware.csv
    with open("auditoria_hardware.csv", "a", newline="") as arq_tickets:
        writer = csv.writer(arq_tickets)
        writer.writerow([mensagem])

def start_suporte_hardware():
    while True:
        try:
            # Conectar ao RabbitMQ no CloudAMQP
            url = "amqps://lqiqnoqf:BXQ-orAqYUGGnXje8uK0h6xRnfXVSSIl@prawn-01.rmq.cloudamqp.com/lqiqnoqf"
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.exchange_declare(exchange='support_ticket_exchange', exchange_type='topic', durable=True)

            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange='support_ticket_exchange', queue=queue_name, routing_key='suporte.hardware')

            print('Suporte esperando por novos tickets de Hardware...')

            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexão com RabbitMQ perdida. Tentando reconectar...")
            time.sleep(5)

start_suporte_hardware()
