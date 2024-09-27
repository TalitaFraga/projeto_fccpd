import os
import csv
import subprocess
import time



AUDITORIA_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria.csv'
AUDITORIA_SOFTWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria_software.csv'
AUDITORIA_HARDWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria_hardware.csv'

LOG_SUPORTE_PATH = 'src/main/java/com/example/projeto_amqp/python/log_suporte.txt'


def adicionar_ticket():
    tipo_suporte = input("Digite 1 se o problema é de Software, 2 se for de Hardware")
    if tipo_suporte == "1":
        routing_key = "suporte.software"
        auditoria_path = AUDITORIA_SOFTWARE_PATH
    elif tipo_suporte == "2":
        routing_key = "suporte.hardware"
        auditoria_path = AUDITORIA_HARDWARE_PATH
    else:
        print("Tipo de suporte inválido. Escolha '1' para Software ou '2' para Hardware.")
        return
    nome_cliente = input("Digite o nome do cliente: ")
    descricao_chamado = input("Digite a descrição do chamado: ")
    routing_key = f"suporte.{tipo_suporte}"
    #os.system(f'java -jar target/projeto_amqp-0.0.1-SNAPSHOT.jar "{routing_key}""{nome_cliente}" "{descricao_chamado}"')
    subprocess.Popen(f'java -jar target/projeto_amqp-0.0.1-SNAPSHOT.jar "{routing_key}" "{nome_cliente}" "{descricao_chamado}"', shell=True)
    print("Chamado adicionado com sucesso.")
    time.sleep(3)

def ver_e_resolver_ticket():
    # Pergunta qual tipo de suporte o operador quer visualizar
    tipo_suporte = input("Digite 1 para ver chamados de Software, 2 para ver chamados de Hardware: ")

    if tipo_suporte == "1":
        suporte_escolhido = "software"
        caminho_log = f'src/main/java/com/example/projeto_amqp/python/log_suporte_software.txt'
    elif tipo_suporte == "2":
        suporte_escolhido = "hardware"
        caminho_log = f'src/main/java/com/example/projeto_amqp/python/log_suporte_hardware.txt'
    else:
        print("Escolha inválida. Por favor, escolha '1' para Software ou '2' para Hardware.")
        return

    try:
        # Abre o arquivo de log correspondente ao tipo de suporte
        with open(caminho_log, 'r', newline='') as file:
            tickets = file.readlines()

        if tickets:
            print(f"\n--- Tickets Pendentes para {suporte_escolhido.capitalize()} ---")
            for idx, ticket in enumerate(tickets, 1):
                print(f"{idx}. {ticket.strip()}")

            escolha = int(input("Digite o número do ticket que deseja resolver: ")) - 1
            if 0 <= escolha < len(tickets):
                nome_analista = input("Digite o nome do Analista: ")
                ticket_resolvido = tickets.pop(escolha)

                resposta = input(f"Digite a resposta para o cliente no ticket: {ticket_resolvido.strip()} ")

                with open(caminho_log, 'a', newline='') as log_file:
                    log_file.write(f"Resolvido: {ticket_resolvido.strip()} | Resolvido por: {nome_analista} - Resposta: {resposta}\n")
                print(f"Ticket resolvido e registrado em {caminho_log}: {ticket_resolvido.strip()}")

                with open(caminho_log, 'w', newline='') as file:
                    file.writelines(tickets)
            else:
                print("Número de ticket inválido.")
        else:
            print(f"Nenhum ticket pendente para {suporte_escolhido.capitalize()}.")
    except FileNotFoundError:
        print(f"Arquivo {caminho_log} não encontrado.")


# Função de menu principal
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1. Abrir Chamado (adicionar ticket)")
        print("2. Ver e Resolver Tickets")
        print("3. Sair")

        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            adicionar_ticket()
        elif escolha == '2':
            ver_e_resolver_ticket()
        elif escolha == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
