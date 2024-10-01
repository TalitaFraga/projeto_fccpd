package com.example.projeto_amqp;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class ClienteProdutor implements CommandLineRunner {

    @Autowired
    private RabbitTemplate rabbitTemplate;

     private static final String EXCHANGE_NAME = "support_ticket_topic_exchange";

    @Override
	public void run(String... args) throws Exception {
	 	if (args.length < 3) {
	 		System.out.println("Uso: java -jar projeto_amqp.jar <routing_key> <nome_cliente> <descricao_chamado>");
	 		return;
	 	}

		// Receber os argumentos do subprocess
		String routingKey = args[0];
		String nomeCliente = args[1];
		// Construa a descrição do chamado juntando todos os argumentos restantes
		StringBuilder descricaoBuilder = new StringBuilder();
		for (int i = 2; i < args.length; i++) {
			descricaoBuilder.append(args[i]).append(" ");
		}
		String descricaoChamado = descricaoBuilder.toString().trim();
		String dataHora = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm"));
		String message = String.format("[%s] Cliente: %s - Descrição: %s", dataHora, nomeCliente, descricaoChamado);

		// Publicar a mensagem no RabbitMQ
		rabbitTemplate.convertAndSend(EXCHANGE_NAME, routingKey, message);

		System.out.println("Mensagem enviada: " + message);
	}
}