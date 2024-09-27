import pika
import csv
from datetime import datetime
import time

def callback(ch, method, properties, body):
    mensagem = body.decode()

    print(f"AUDITORIA SOFTWARE: Mensagem recebida - {mensagem}")

    # Escrever no arquivo auditoria_software.csv
    with open("auditoria_software.csv", "a", newline="") as arq_tickets:
        writer = csv.writer(arq_tickets)
        writer.writerow([mensagem])

def start_auditoria_software():
    while True:
        try:
            # Conectar ao RabbitMQ no CloudAMQP
            url = "amqps://lqiqnoqf:BXQ-orAqYUGGnXje8uK0h6xRnfXVSSIl@prawn-01.rmq.cloudamqp.com/lqiqnoqf"
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            # Declarar o exchange como 'topic'
            channel.exchange_declare(exchange='support_ticket_exchange', exchange_type='topic', durable=True)

            # Declarar uma fila temporária para o backend de auditoria de software
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            # Associar a fila ao exchange, escutando apenas mensagens de 'software'
            channel.queue_bind(exchange='support_ticket_exchange', queue=queue_name, routing_key='suporte.software')

            print('Backend de auditoria para Software esperando por mensagens...')

            # Configurar o consumidor
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            # Iniciar o consumo
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexão com RabbitMQ perdida. Tentando reconectar...")
            time.sleep(5)  # Espera 5 segundos antes de tentar reconectar

start_auditoria_software()
