# Importa as perguntas organizadas por tema, em formato de dicionários
from perguntas import perguntas_por_tema

# Classe que representa uma pergunta do quiz
class Pergunta:
    def __init__(self, texto, alternativas, correta):
        self.texto = texto                      # Enunciado da pergunta
        self.alternativas = alternativas        # Lista com as alternativas de resposta
        self.correta = correta                  # Índice da alternativa correta

    # Método que verifica se o índice passado corresponde à resposta correta
    def esta_correta(self, indice):
        return indice == self.correta           # Retorna True se o índice for igual ao índice da resposta correta

# Dicionário que armazenará as perguntas já convertidas em objetos da classe Pergunta, separadas por tema
questoes_por_tema = {}

# Percorre cada tema e suas respectivas perguntas
for tema, lista in perguntas_por_tema.items():
    # Para cada tema, cria uma lista de objetos Pergunta a partir da lista de dicionários
    questoes_por_tema[tema] = [
        Pergunta(
            texto=p["texto"],                  # Enunciado da pergunta
            alternativas=p["alternativas"],    # Lista de alternativas
            correta=p["correta"]               # Índice da alternativa correta
        )
        for p in lista                         # Para cada dicionário de pergunta na lista do tema atual
    ]