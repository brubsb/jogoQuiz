from perguntas import perguntas_por_tema

class Pergunta:
    def __init__(self, texto, alternativas, correta):
        self.texto = texto
        self.alternativas = alternativas
        self.correta = correta

    def esta_correta(self, indice):
        return indice == self.correta

# Converte os dicionários em objetos Pergunta separados por tema
questoes_por_tema = {}

for tema, lista in perguntas_por_tema.items():
    questoes_por_tema[tema] = [
        Pergunta(
            texto=p["texto"],
            alternativas=p["alternativas"],
            correta=p["correta"]
        )
        for p in lista
    ]
