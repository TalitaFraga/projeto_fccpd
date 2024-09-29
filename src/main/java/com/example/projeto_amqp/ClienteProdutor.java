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
        if (args.length >= 3) {
            String tipoSuporte = args[0];
            String nomeCliente = args[1];
            StringBuilder chamadoBuilder = new StringBuilder();
            for (int i = 2; i < args.length; i++) {
                chamadoBuilder.append(args[i]).append(" ");
            }
            String chamado = chamadoBuilder.toString().trim();

            String dataHora = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy - HH:mm"));

            String mensagem = "[" + dataHora + "] " + nomeCliente + ": " + chamado;

            String routingKey = "suporte." + tipoSuporte.toLowerCase(); 

            rabbitTemplate.convertAndSend(EXCHANGE_NAME, routingKey, mensagem);
            System.out.println("Chamado de suporte enviado com sucesso: " + mensagem);
        } else {
            System.out.println("É necessário fornecer o nome do cliente e a descrição do chamado.");
        }
    }
}