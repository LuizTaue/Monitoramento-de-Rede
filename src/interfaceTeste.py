import customtkinter as ctk
import os
from dotenv import load_dotenv

diretorio_atual = os.path.dirname(__file__)
caminho_raiz = os.path.join(diretorio_atual, "..")
load_dotenv(os.path.join(caminho_raiz, ".env"))
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
caminhoDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
arquivoConfig = os.path.join(caminhoDesktop, 'configuração_de_tempo_checagem.txt')

class App(ctk.CTk):




    def __init__(self):
        super().__init__()

        #Configuração da Janelaa

        self.title("Monitoramento Lavanderia v2.0")
        self.geometry("500x400")

        # Titulo principal

        self.Titulo = ctk.CTkLabel(self, text="Painel De Controle", font=("Roboto", 24, "bold"))
        self.Titulo.pack(pady=(20,10))

        # Status

        self.listaMaquinas = ["ip01", "ip02", "ip03", "ip04", "ip05"]

        self.statusLeds = {}

        self.frameStatus = ctk.CTkFrame(self)
        self.frameStatus.pack(pady=10, padx=20, fill="both", expand="True")

        for nome in self.listaMaquinas:

            linha = ctk.CTkFrame(self.frameStatus, fg_color="transparent")
            linha.pack(fill="x", pady=5, padx=10)

            CNome = ctk.CTkLabel(linha, text=nome, font=("Roboto", 14))
            CNome.pack(side="left")



            led = ctk.CTkLabel(linha, text="●", text_color="gray", font=("Roboto", 24))
            led.pack(side="right")

            self.statusLeds[nome] = led

        # Campo pra mudar o tempo (INPUT DO CODIGO)

        self.tempo = ctk.CTkLabel(self, text="Tempo de checagem (minutos):")
        self.tempo.pack(pady=(10, 0))
        
        self.entradaTempo = ctk.CTkEntry(self, placeholder_text="Ex: 15")
        self.entradaTempo.pack(pady=5)

        #Botão de Salvar
        self.botaoSalvar = ctk.CTkButton(self, text="Salvar Configuração", command=self.salvar_config)
        self.botaoSalvar.pack(pady=20)

    def salvar_config(self):
        # Pega o valor que o usuario digitou na caixa
        novoTempo = self.entradaTempo.get()
        #print(f"Novo tempo salvo: {novoTempo} minutos")

        # Verifica se o usuario digitou apenas numeros
        if novoTempo.isdigit():
            try:
                # Abre o arquivo em modo de escrita ('w') e salva
                with open(arquivoConfig, "w") as f:
                    f.write(novoTempo)

                print(f"Sucesso! Tempo alterado para {novoTempo} minutos.")
            except Exception as e:
                print(f" Erro ao salvar o arquivo: {e}")    
        else:
            print("Por favor, digite apenas numeros inteiros!")            


if __name__ == "__main__":
    app = App()
    app.mainloop()    