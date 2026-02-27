import subprocess
import time
import pywhatkit as kit # nova biblioteca integração com whatsapp
import requests
import os
from dotenv import load_dotenv



# Configurações

diretorio_atual = os.path.dirname(__file__)
caminho_raiz = os.path.join(diretorio_atual, "..")
load_dotenv(os.path.join(caminho_raiz, ".env"))
caminhoDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
arquivoConfig = os.path.join(caminhoDesktop, 'configuração_de_tempo_checagem.txt')
load_dotenv()
token = os.getenv("TOKEN_BOT")
chat_id = os.getenv("ID_CHAT")
donoDaLavanderia = "Jason"

# Ips definidos
dispositivos = {
    #"ip01": "TOTEM DE PAGAMENTO",
    #"ip02": "MAQUINA 01",
    "ip03": "MAQUINA 02", # teste com o ip do meu celular
    "ip04": "MAQUINA 03", # gateway do meu modem pra teste
    #"ip05": "MAQUINA 04"
}

estadosAnteriores = {ip: True for ip in dispositivos}

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

    

    print(f"\nIniciando Checagem de {minutos} em {minutos} minuto(s):----{time.strftime('%H:%M:%S')} ---")
    print("Pressione Ctrl + c para parar o programa.")
    
    for ip, nome in dispositivos.items():
        comando = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
        onlineAgora = (comando.returncode == 0)

        # Ficou Offline
        if not onlineAgora and estadosAnteriores[ip]:
            print(f"❌ {nome} ({ip}) Está OFFLINE!")

            with open("logLavanderia.txt", "a") as arquivo:
                arquivo.write(f"{time.strftime('%d/%m/%Y %H:%M:%S')} - ERRO: {nome} fora do ar\n")

                mensagem = f"*ALERTA:* {donoDaLavanderia}, a *{nome}* parou de responder! ⚠️"
                enviarTelegram(mensagem)
                estadosAnteriores[ip] = False #atualiza a memoria para off

        # Ficou online
        elif onlineAgora and not estadosAnteriores[ip]:
            print(f"✅ {nome} ({ip}) VOLTOU A FICAR ONLINE!")

            mensagem = f"🎉 *BOAS NOTÍCIAS:* {donoDaLavanderia}, a *{nome}* está online novamente!"
            enviarTelegram(mensagem)
            estadosAnteriores[ip] = True # Atualiza a memoria para on

        else:

            status = "Online" if onlineAgora else "Offline"
            print(f"ℹ️ {nome}: Mantém-se {status}")    

            # kit.sendwhatmsg_instantly("+5531995551028", mensagem, wait_time=15, tab_close=True)

print(f"Olá! O sistema de monitoramento da lavanderia do {donoDaLavanderia} está pronto.")

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

estavaOnline = True

while True:
    
    minutos = configTempo()
    verificar_maquinas()

    print(f"\n Aguardando {minutos} minuto(s) para a próxima checagem...")
    time.sleep(minutos * 60)
             