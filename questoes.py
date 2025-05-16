from perguntas import perguntas  # Importa a lista de dicionários de perguntas

# Classe que representa uma pergunta do quiz
class Pergunta:
    def __init__(self, texto, alternativas, correta):
        self.texto = texto                     # Enunciado da pergunta
        self.alternativas = alternativas       # Lista com 4 alternativas
        self.correta = correta                 # Índice da resposta correta

    # Verifica se a alternativa escolhida pelo jogador está correta
    def esta_correta(self, indice):
        return indice == self.correta


# Transforma os dicionários em objetos Pergunta
# Isso deixa o código mais organizado e orientado a objetos
questoes = []
for p in perguntas:
    pergunta_obj = Pergunta(
        texto=p["texto"],
        alternativas=p["alternativas"],
        correta=p["correta"]
    )
    questoes.append(pergunta_obj)
