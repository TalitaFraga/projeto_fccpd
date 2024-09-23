import os
import csv

AUDITORIA_PATH = 'src/main/java/com/example/projeto_amqp/python/auditoria.csv'
LOG_SUPORTE_PATH = 'src/main/java/com/example/projeto_amqp/python/log_suporte.txt'


def adicionar_ticket():
    nome_cliente = input("Digite o nome do cliente: ")
    descricao_chamado = input("Digite a descrição do chamado: ")
    
    os.system(f'java -jar target/projeto_amqp-0.0.1-SNAPSHOT.jar "{nome_cliente}" "{descricao_chamado}"')
    print("Chamado adicionado com sucesso.")
    

def ver_e_resolver_ticket():
    try:
        with open(AUDITORIA_PATH, 'r', newline='') as file:
            tickets = file.readlines()

        if tickets:
            print("\n--- Tickets Pendentes ---")
            for idx, ticket in enumerate(tickets, 1):
                print(f"{idx}. {ticket.strip()}") 
            
            escolha = int(input("Digite o número do ticket que deseja resolver: ")) - 1
            if 0 <= escolha < len(tickets):
                ticket_resolvido = tickets.pop(escolha)
                
                resposta = input(f"Digite a resposta para o cliente no ticket: {ticket_resolvido.strip()} ")

                with open(LOG_SUPORTE_PATH, 'a', newline='') as log_file:
                    log_file.write(f"Resolvido: {ticket_resolvido.strip()} - Resposta: {resposta}\n")
                print(f"Ticket resolvido e registrado em log_suporte.txt: {ticket_resolvido.strip()}")

                with open(AUDITORIA_PATH, 'w', newline='') as file:
                    file.writelines(tickets)
            else:
                print("Número de ticket inválido.")
        else:
            print("Nenhum ticket pendente.")
    except FileNotFoundError:
        print(f"Arquivo {AUDITORIA_PATH} não encontrado.")

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
