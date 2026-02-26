Monitor de Rede - Lavanderia 24 horas


Criei esse script para resolver um problema real em uma lavanderia de autoatendimento recem aberta por um amigo. 
A dúvida do mesmo era: "Como vou saber se algum equipamento perder o sinal?"
A partir dessa dúvida, eu iniciei o processo de criação da minha primeira automação utilizando os equipamentos do meu espaço pessoal, visando a resolução desse possivel problema.

O que ele faz:
Checagem em tempo real: Fica pingando o ip do meu modem e smartphone para ver se a internet está ativa.

Aviso no Telegram: Se cair, ele manda um alerta no telegram.

Configuração fácil: Criei uma integração que lê um arquivo .txt na Área de Trabalho. Assim, o dono da lavanderia pode mudar o tempo de checagem (ex: de 5 para 10 minutos) sem precisar abrir o código ou me chamar.

Roda escondido: Transformei o script em um executável (.exe) que inicia junto com o Windows e fica rodando em segundo plano.

Como usar:
Configure as variáveis no arquivo .env.

Gere o executável com o PyInstaller.

Coloque o .exe para iniciar com o Windows (Agendador de Tarefas).

O arquivo configuracao_de_tempo_checagem.txt será criado automaticamente na Área de Trabalho do usuário.

Tecnologias utilizadas:

Python 3

Requests (para falar com o Telegram)

Dotenv (para não subir senhas no GitHub)

PyInstaller (para virar um programa de Windows)


Atualização: Agora o sistema também notifica quando a conexão é reestabelecida.

Atualização: Interface gráfica (GUI) implementada com sucesso, permitindo o controle visual do monitoramento e ajuste de configurações de tempo.