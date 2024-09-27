package com.example.projeto_amqp;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ProjetoAmqpApplication implements CommandLineRunner {

	@Autowired
	private RabbitTemplate rabbitTemplate;

	public static void main(String[] args) {
		SpringApplication.run(ProjetoAmqpApplication.class, args);
	}

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
		String message = String.format("Cliente: %s - Descrição: %s", nomeCliente, descricaoChamado);

		// Publicar a mensagem no RabbitMQ
		rabbitTemplate.convertAndSend("support_ticket_exchange", routingKey, message);

		System.out.println("Mensagem enviada: " + message);
	}
}
