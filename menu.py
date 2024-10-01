import os
import subprocess
import time

AUDITORIA_SOFTWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria_software.csv'
AUDITORIA_HARDWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria_hardware.csv'
LOG_SUPORTE_SOFTWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/log_suporte_software.txt'
LOG_SUPORTE_HARDWARE_PATH = 'src/main/java/com/example/projeto_amqp/python/log_suporte_hardware.txt'


def adicionar_ticket():
    tipo_suporte = input("Digite 1 para problema de Software ou 2 para Hardware: ")
    if tipo_suporte == '1':
        routing_key = "suporte.software"
    elif tipo_suporte == '2':
        routing_key = "suporte.hardware"
    else:
        print("Opção inválida!")
        return

    nome_cliente = input("Digite o nome do cliente: ")
    descricao_chamado = input("Digite a descrição do chamado: ")
    
    # Executar o comando Java para abrir o ticket
    subprocess.Popen(f'java -jar target/projeto_amqp-0.0.1-SNAPSHOT.jar "{routing_key}" "{nome_cliente}" "{descricao_chamado}"', shell=True)
    
    print("Chamado adicionado com sucesso.")
    time.sleep(3)


def ver_e_resolver_ticket():
    tipo_suporte = input("Digite 1 para ver chamados de Software, 2 para Hardware: ")

    if tipo_suporte == '1':
        auditoria_path = AUDITORIA_SOFTWARE_PATH
        log_suporte_path = LOG_SUPORTE_SOFTWARE_PATH
    elif tipo_suporte == '2':
        auditoria_path = AUDITORIA_HARDWARE_PATH
        log_suporte_path = LOG_SUPORTE_HARDWARE_PATH
    else:
        print("Opção inválida!")
        return

    try:
        # Abrir o arquivo CSV correspondente para ver os tickets
        with open(auditoria_path, 'r', newline='') as file:
            tickets = file.readlines()

        if tickets:
            print("\n--- Tickets Pendentes ---")
            for idx, ticket in enumerate(tickets, 1):
                print(f"{idx}. {ticket.strip()}")  # Exibe a linha completa do ticket
            
            escolha = int(input("Digite o número do ticket que deseja resolver: ")) - 1
            if 0 <= escolha < len(tickets):
                nome_analista = input("Digite o nome do Analista: ")
                ticket_resolvido = tickets.pop(escolha)
                
                resposta = input(f"Digite a resposta para o cliente no ticket: {ticket_resolvido.strip()} ")

                # Gravar a resposta no arquivo de log correspondente
                with open(log_suporte_path, 'a', newline='') as log_file:
                    log_file.write(f"Resolvido: {ticket_resolvido.strip()} | Resolvido por: {nome_analista} - Resposta: {resposta} \n")
                print(f"Ticket resolvido e registrado em {log_suporte_path}: {ticket_resolvido.strip()}")

                # Atualizar o arquivo de auditoria, removendo o ticket resolvido
                with open(auditoria_path, 'w', newline='') as file:
                    file.writelines(tickets)
            else:
                print("Número de ticket inválido.")
        else:
            print("Nenhum ticket pendente.")
    except FileNotFoundError:
        print(f"Arquivo {auditoria_path} não encontrado.")


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
