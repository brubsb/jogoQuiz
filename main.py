# Importa a biblioteca Flet para construir a interface visual
import flet as ft

# Importa biblioteca padrão do Python para leitura e gravação de arquivos CSV
import csv

# Importa as classes e dados do seu projeto
from quiz_controller import QuizController  # Controla o funcionamento do quiz
from jogador import Jogador                 # Representa o jogador e sua pontuação
from questoes import questoes              # Lista com as perguntas do quiz

# Função principal que será chamada para rodar o aplicativo
def main(page: ft.Page):
    # Define título e tamanho da janela do aplicativo
    page.title = "Quiz em Flet"
    page.window_width = 600
    page.window_height = 500

    # Cria um jogador vazio (nome será definido depois)
    jogador = Jogador(nome="")

    # Cria o controlador que gerencia o quiz com perguntas e jogador
    controller = QuizController(perguntas=questoes, jogador=jogador)

    # Campo de texto para o jogador digitar o nome
    nome_input = ft.TextField(label="Digite seu nome")

    # Botão para iniciar o quiz
    iniciar_btn = ft.ElevatedButton(text="Iniciar Quiz")

    # Função chamada quando o botão "Iniciar Quiz" é clicado
    def iniciar_quiz(e):

        jogador.nome = nome_input.value.strip()  # Pega o nome do campo de texto

        # Valida se o nome foi digitado
        if not jogador.nome:
            page.snack_bar = ft.SnackBar(ft.Text("Digite um nome!"))
            page.snack_bar.open = True
            page.update()
            return

        # Começa o quiz mostrando a primeira pergunta
        mostrar_pergunta()

    # Associa a função acima ao botão
    iniciar_btn.on_click = iniciar_quiz

    # Exibe a pergunta atual na tela
    def mostrar_pergunta(e=None):
        page.controls.clear()  # Limpa a tela antes de adicionar a nova pergunta

        # Verifica se o quiz já terminou (todas as perguntas respondidas)
        if controller.quiz_finalizado():
            salvar_resultado()   # Salva o resultado no arquivo
            mostrar_resultado()  # Mostra pontuação final + histórico
            return

        # Pega a pergunta atual
        pergunta = controller.obter_pergunta_atual()

        # Adiciona o texto da pergunta à tela
        page.controls.append(ft.Text(pergunta.texto, size=20, weight="bold"))

        # Para cada alternativa, cria um botão
        for i, alt in enumerate(pergunta.alternativas):
            btn = ft.ElevatedButton(text=alt)
            # Cada botão chama a função responder passando o índice da alternativa
            btn.on_click = lambda e, idx=i: responder(idx)
            page.controls.append(btn)

        page.update()

    # Lógica para responder uma pergunta
    def responder(indice):
        controller.responder(indice)  # Verifica se está certo e avança no quiz
        mostrar_pergunta()            # Atualiza a tela com a próxima pergunta

    # Grava o nome e a pontuação do jogador no arquivo CSV
    def salvar_resultado():
        try:
            # Abre (ou cria) o arquivo "resultados.csv" em modo de adição ("a")
            with open("resultados.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)  # Cria um objeto para escrever no CSV
                escritor.writerow([jogador.nome, jogador.pontuacao])  # Escreve uma linha com nome e pontos
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")  # Se der erro, mostra no console

    # Lê o arquivo "resultados.csv" e devolve os dados como lista de tuplas (nome, pontuação)
    def carregar_resultados():
        resultados = []
        try:
            # Abre o arquivo em modo leitura
            with open("resultados.csv", "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.reader(arquivo)  # Cria um leitor de CSV
                for linha in leitor:
                    if len(linha) == 2:
                        nome, pontos = linha
                        resultados.append((nome, pontos))  # Adiciona à lista
        except FileNotFoundError:
            pass  # Ignora se o arquivo ainda não existe (primeira vez jogando)
        return resultados  # Retorna a lista de resultados

    # Exibe a pontuação do jogador e o histórico
    def mostrar_resultado():
        page.controls.clear()

        # Mostra a pontuação do jogador atual
        page.controls.append(
            ft.Text(f"Pontuação: {jogador.pontuacao}", size=22, color="green")
        )

        # Título da seção de histórico
        page.controls.append(ft.Text("🏅 Históricos anteriores:", size=18, weight="bold"))

        # Carrega os resultados gravados anteriormente
        historico = carregar_resultados()

        if historico:
            # Mostra os últimos 5 resultados gravados
            for nome, pontos in historico[-5:]:
                page.controls.append(ft.Text(f"{nome}: {pontos} pontos"))
        else:
            page.controls.append(ft.Text("Nenhum resultado salvo ainda."))

        def reiniciar_quiz(e=None):
            # Reinicia jogador e controlador
            jogador.nome = ""
            jogador.pontuacao = 0
            controller.reiniciar()

            # Limpa a tela e volta ao início (campo de nome + botão)
            page.controls.clear()
            page.controls.append(nome_input)
            page.controls.append(iniciar_btn)
            page.update()

        # Botão de reinício
        page.controls.append(
            ft.ElevatedButton(text="Jogar novamente", on_click=reiniciar_quiz)
        )

        page.update()

    # Adiciona os elementos iniciais à página (campo e botão)
    page.controls.append(nome_input)
    page.controls.append(iniciar_btn)
    page.update()


# Inicia o aplicativo chamando a função main
ft.app(target=main)