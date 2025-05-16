from questoes import questoes  # Importa a lista de objetos Pergunta

# Classe que controla o funcionamento do quiz
class QuizController:
    def __init__(self, perguntas, jogador):
        self.perguntas = perguntas     # Lista de perguntas do quiz
        self.jogador = jogador         # Objeto Jogador que está jogando
        self.indice_atual = 0          # Índice da pergunta atual

    # Retorna a pergunta atual com base no índice
    def obter_pergunta_atual(self):
        return self.perguntas[self.indice_atual]

    # Processa a resposta do jogador
    def responder(self, indice_escolhido):
        pergunta = self.obter_pergunta_atual()

        # Se a resposta estiver correta, soma 1 ponto
        if pergunta.esta_correta(indice_escolhido):
            self.jogador.pontuar()

        # Avança para a próxima pergunta
        self.indice_atual += 1

    # Verifica se o quiz acabou (todas as perguntas respondidas)
    def quiz_finalizado(self):
        return self.indice_atual >= len(self.perguntas)
    
    def reiniciar(self):
        self.indice_atual = 0
        self.jogador.pontuacao = 0

