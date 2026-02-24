import subprocess
import time
import pywhatkit as kit # nova biblioteca integração com whatsapp
import requests
import os
from dotenv import load_dotenv



# Configurações

caminhoDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
arquivoConfig = os.path.join(caminhoDesktop, 'configuração_de_tempo_checagem.txt')
load_dotenv()
token = os.getenv("TOKEN_BOT")
chat_id = os.getenv("ID_CHAT")
donoDaLavanderia = "Jason"

# Ips definidos
dispositivos = {
    "192.168.1.20": "TOTEM DE PAGAMENTO",
    "192.168.1.51": "MAQUINA 01",
    "192.168.18.93": "MAQUINA 02", # teste com o ip do meu celular
    "192.168.18.1": "MAQUINA 03", # gateway do meu modem pra teste
    "192.168.1.54": "MAQUINA 04"
}


def enviarTelegram(mensagem):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
                "chat_id": chat_id, 
                "text": mensagem, 
                "parse_mode": "Markdown"
    }
    
    try:       
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erro ao enviar telegram: {e}")    



def verificar_maquinas():

    

    print(f"\n------Entendido - Iniciando Checagem de {minutos} em {minutos} minuto(s): ------{time.strftime('%H:%M:%S')} ---")
    print("Pressione Ctrl + c para parar o programa.")
    
    for ip, nome in dispositivos.items():
        # O comando 'ping' envia um sinal e espera resposta
        # '-n 1' envia apenas 1 pacote para ser rápido
        # '-w 500' espera meio segundo pela resposta
        comando = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
        
        if comando.returncode == 0:
            print(f"✅ {nome} ({ip}) está Online.")
        else:
            print(f"❌ ATENÇÃO: {nome} ({ip}) ESTÁ OFFLINE!")
            # da pra colocar o código para enviar um WhatsApp

            with open("logLavanderia.txt", "a") as arquivo:
                    arquivo.write(f"{time.strftime('%d/%m/%Y %H:%M:%S')} - ERRO: {nome} ({ip}) fora do ar\n")

            mensagem = f"⚠️*ALERTA DO SISTEMA:* {donoDaLavanderia}, {nome} ip ({ip}) parou de responder! ⚠️"
            enviarTelegram(mensagem)

            # kit.sendwhatmsg_instantly("+5531995551028", mensagem, wait_time=15, tab_close=True)


#print(f"Olá! O sistema de monitoramento da lavanderia do {donoDaLavanderia} está pronto.")
#minutos = input("De quantos em quantos minutos devo checar as máquinas?  ")
#intervaloSegundos = int(minutos) * 60

def configTempo():

    # se o arquivo nao existir, o proprio codigo vai cria-lo, assumindo que é 15 minutos por padrão.
    if not os.path.exists(arquivoConfig):
        with open(arquivoConfig, "w") as f:
            f.write("15")
            return 15

    #se existir um txt ele só lê o que esta dentro
    try:
        with open(arquivoConfig, "r") as f:
            conteudo = f.read().strip()
            return int(conteudo)
    except:
        return 15 # caso alguem escreva algo errado no txt, ele ja assume que é 15                

#minutos = configTempo()
#intervaloSegundos = int(minutos) * 60

#print(f" Configuração carregada: Checagem a cada {minutos} minuto(s).")

while True:
    
    minutos = configTempo()
    intervaloSegundos = int(minutos) * 60

    verificar_maquinas()
    print(f"\n Aguardando {minutos} minuto(s) para a próxima checagem...")
    time.sleep(intervaloSegundos)