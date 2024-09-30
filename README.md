# Sistema de Suporte para Empresa de TI

#### Este projeto implementa um sistema de suporte para uma empresa de TI, onde clientes podem abrir tickets de suporte para problemas relacionados a hardware ou software. O sistema conta com dois tipos de suporte: um para hardware e outro para software. Além disso, todas as mensagens são registradas em um sistema de auditoria que monitora os tickets.

## Estrutura

- **ClienteProdutor**: Gera e envia os tickets de suporte
- **Consumidores**: Um consumidor para hardware e outro para software, que recebem os tickets e resolvem os problemas
- **Auditoria**: Registra todos os tickets de suporte enviados, separados por tipo (hardware e software)

## Requisitos

- **Java**: Para o produtor de mensagens
- **Python**: Para os consumidores e auditoria
- **RabbitMQ**: Para o gerenciamento de mensagens (CloudAMQP configurado)
- **Maven**: Para compilar e rodar o projeto Java

## Instalação e Execução

Clone o projeto:

```sh
git clone https://github.com/TalitaFraga/projeto_fccpd.git
```
## Configurar o RabbitMQ
Configure o RabbitMQ utilizando as credenciais fornecidas pelo serviço CloudAMQP

## Executar os Consumidores (Python)
Acessar a pasta python e executar no terminal
Para consumidor software:
```sh
 python3 consumidor_software.py
```
Para consumidor hardware:
```sh
python3 consumidor_hardware.py 
```


## Executar o Backend de Auditoria (Python)
Acessar a pasta python e executar:
```sh
python3 auditoria.py
```

## Executando o menu
Na pasta raiz do projeto executar no terminal:
```sh
python3 menu.py
```
O menu aparecerá o terminal. Você será capaz de abrir novos chamados de hardware ou software, resolver tickets ou sair do menu.

## Arquivos de Auditoria
Os chamados são resgistrados em dois arquivos: auditoria_software.csv para problemas de software e auditoria_hardware.csv para problemas de hardware.
Os chamados resolvidos são resgistrados em dois arquivos: log_suporte_hardware.txt para problemas de hardware e log_suporte_software.txt para problemas de software


Se estiver usando macOS/Linux execute python3 + nome do arquivo. Windows use python + nome do arquivo