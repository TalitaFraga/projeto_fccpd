import pika
import csv
import time


AUDITORIA_SOFTWARE_PATH = 'auditoria_software.csv'
AUDITORIA_HARDWARE_PATH = 'auditoria_hardware.csv'

def callback(ch, method, properties, body):
    mensagem = body.decode()
    routing_key = method.routing_key

    if routing_key == 'suporte.software':
        print(f"AUDITORIA SOFTWARE: Mensagem recebida - {mensagem}")
        with open(AUDITORIA_SOFTWARE_PATH, 'a', newline='') as arq_tickets:
            writer = csv.writer(arq_tickets)
            writer.writerow([mensagem])
    elif routing_key == 'suporte.hardware':
        print(f"AUDITORIA HARDWARE: Mensagem recebida - {mensagem}")
        with open(AUDITORIA_HARDWARE_PATH, 'a', newline='') as arq_tickets:
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

            # Declarar o exchange como 'topic'
            channel.exchange_declare(exchange='support_ticket_topic_exchange', exchange_type='topic', durable=True)

            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            # Associar a fila ao exchange para receber tanto software quanto hardware
            channel.queue_bind(exchange='support_ticket_topic_exchange', queue=queue_name, routing_key='suporte.software')
            channel.queue_bind(exchange='support_ticket_topic_exchange', queue=queue_name, routing_key='suporte.hardware')

            print('Backend de auditoria esperando por mensagens...')

            # Configurar o consumidor
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            # Iniciar o consumo
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Conexão com RabbitMQ perdida. Tentando reconectar...")
            time.sleep(5)

start_auditoria()
