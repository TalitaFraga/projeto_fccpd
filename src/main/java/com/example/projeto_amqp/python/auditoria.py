import pika
import csv
from datetime import datetime
import time

def callback(ch, method, properties, body):
    mensagem = body.decode()
    
    print(f"AUDITORIA: Mensagem recebida - {mensagem}")

    with open("auditoria.csv", "a", newline="") as arq_tickets:
        writer = csv.writer(arq_tickets)
        writer.writerow([mensagem])

def start_auditoria():
    while True:
        try:
            # Conectar ao RabbitMQ no CloudAMQP
            url = "amqps://lqiqnoqf:BXQ-orAqYUGGnXje8uK0h6xRnfXVSSIl@prawn-01.rmq.cloudamqp.com/lqiqnoqf"
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            # Declarar o exchange como durável
            channel.exchange_declare(exchange='support_ticket_exchange', exchange_type='fanout', durable=True)

            # Declarar uma fila temporária para o backend de auditoria
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            # Associar a fila ao exchange
            channel.queue_bind(exchange='support_ticket_exchange', queue=queue_name)

            print('Backend de auditoria esperando por mensagens...')

            # Configurar o consumidor
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            # Iniciar o consumo
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexão com RabbitMQ perdida. Tentando reconectar...")
            time.sleep(5)  # Espera 5 segundos antes de tentar reconectar

start_auditoria()
