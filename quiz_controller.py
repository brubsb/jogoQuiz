class QuizController:
    def __init__(self, perguntas, jogador):
        self.perguntas = perguntas  # Lista de perguntas selecionadas
        self.jogador = jogador
        self.indice_atual = 0

    def reiniciar(self):
        self.indice_atual = 0
        self.jogador.pontuacao = 0

    def obter_pergunta_atual(self):
        return self.perguntas[self.indice_atual]

    def responder(self, indice_resposta):
        pergunta = self.obter_pergunta_atual()
        if pergunta.esta_correta(indice_resposta):
            self.jogador.pontuacao += 1
        self.indice_atual += 1

    def quiz_finalizado(self):
        return self.indice_atual >= len(self.perguntas)
