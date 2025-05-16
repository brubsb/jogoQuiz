# Classe que representa um jogador no quiz
class Jogador:
    def __init__(self, nome):
        self.nome = nome            # Nome do jogador
        self.pontuacao = 0          # Pontuação inicial começa em 0

    # Método para adicionar 1 ponto quando a resposta está correta
    def pontuar(self):
        self.pontuacao += 1
