# Classe que controla o funcionamento do quiz
class QuizController:
    def __init__(self, perguntas, jogador):
        self.perguntas = perguntas      # Lista de perguntas sorteadas para o quiz
        self.jogador = jogador          # Jogador que está participando
        self.indice_atual = 0           # Índice da pergunta atual (começa na primeira)

    # Reinicia o quiz, útil para quando o jogador quiser jogar novamente
    def reiniciar(self):
        self.indice_atual = 0               # Volta para a primeira pergunta
        self.jogador.pontuacao = 0          # Zera a pontuação do jogador

    # Retorna a pergunta atual com base no índice
    def obter_pergunta_atual(self):
        return self.perguntas[self.indice_atual]

    # Método que trata a resposta do jogador
    def responder(self, indice_resposta):
        pergunta = self.obter_pergunta_atual()  # Pega a pergunta atual

        # Verifica se a resposta escolhida pelo jogador está correta
        if pergunta.esta_correta(indice_resposta):
            # Se estiver correta, soma 1 ponto à pontuação do jogador
            self.jogador.pontuacao += 1

        # Independente de estar certa ou errada, avança para a próxima pergunta
        self.indice_atual += 1

    # Verifica se o quiz chegou ao fim
    def quiz_finalizado(self):
        # O quiz acaba quando o índice atual for igual ou maior que o número total de perguntas
        return self.indice_atual >= len(self.perguntas)