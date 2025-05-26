import flet as ft  # Biblioteca para criar interfaces gráficas
import csv  # Leitura e escrita de arquivos CSV
import random  # Sorteio aleatório de itens (ex: perguntas)
import asyncio  # Execução de tarefas assíncronas (ex: delays)
from quiz_controller import QuizController  # Lógica do quiz (perguntas, respostas, pontuação)
from jogador import Jogador  # Classe que representa o jogador
from questoes import questoes_por_tema  # Dicionário com perguntas organizadas por tema


def main(page: ft.Page):
    # Configurações iniciais da janela do aplicativo
    page.title = "Quiz em Flet"
    page.window_width = 600
    page.window_height = 500
    page.bgcolor = "#ccdceb"  # Cor de fundo da janela

    jogador = Jogador(nome="")  # Instância do jogador, começa com nome vazio
    controller = None           # Controlador do quiz, inicializado como None
    tema_selecionado = None    # Guarda o tema escolhido pelo usuário

    # Campo para digitar o nome do jogador
    nome_input = ft.TextField(
        label="Digite seu nome",
        width=300,
        bgcolor="#5483b3,0.2",  # Cor de fundo com transparência
        height=70,
        color="#ffffff",
        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_400)
    )

    # Botão para iniciar o quiz após escolher nome e tema
    iniciar_btn = ft.ElevatedButton(
        text="Iniciar Quiz",
        bgcolor="#052659,0.6",  # Cor de fundo com transparência
        color="#ffffff",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
            shape=ft.RoundedRectangleBorder(radius=20),  # Botão com cantos arredondados
            padding=20
        )
    )

    # Função que cria o botão de voltar para a tela inicial (ícone de casa)
    def botao_voltar():
        return ft.IconButton(
            icon=ft.Icons.HOME,
            icon_size=40,
            height=50,
            icon_color="#052659,0.7",  # Cor do ícone com transparência
            tooltip="Voltar para a página inicial",  # Texto ao passar mouse
            on_click=lambda e: mostrar_tela_inicial()  # Ação ao clicar: volta à tela inicial
        )

    # Função que mostra a tela inicial com opções de tema para o quiz
    def mostrar_tela_inicial(e=None):
        page.controls.clear()  # Limpa todos os controles da tela para atualizar
        page.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Bem-vindo ao Quiz!",
                                size=45,
                                weight=ft.FontWeight.W_700,
                                height=60,
                                color="#57689e",
                                text_align=ft.TextAlign.CENTER),
                        ft.Text("Escolha um tema para começar:", size=20, weight=ft.FontWeight.W_500, height=50),
                        # Botões para selecionar os temas: curiosidades, música, lógica
                        ft.ElevatedButton(text="Curiosidades Gerais",
                                          on_click=lambda e: selecionar_tema("curiosidades"),
                                          bgcolor=ft.Colors.WHITE,
                                          color="#57689e",
                                          width=250,
                                          height=40,
                                          style=ft.ButtonStyle(
                                              text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                                              shape=ft.RoundedRectangleBorder(radius=15),
                                              padding=6)
                                          ),
                        ft.ElevatedButton(text="Música",
                                          on_click=lambda e: selecionar_tema("musica"),
                                          bgcolor=ft.Colors.WHITE,
                                          color="#57689e",
                                          width=250,
                                          height=40,
                                          style=ft.ButtonStyle(
                                              text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                                              shape=ft.RoundedRectangleBorder(radius=15),
                                              padding=6)
                                          ),
                        ft.ElevatedButton(text="Pegadinhas e Lógica",
                                          on_click=lambda e: selecionar_tema("logica"),
                                          bgcolor=ft.Colors.WHITE,
                                          color="#57689e",
                                          width=250,
                                          height=40,
                                          style=ft.ButtonStyle(
                                              text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                                              shape=ft.RoundedRectangleBorder(radius=15),
                                              padding=6)
                                          ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente os elementos
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
                    expand=True  # Faz a coluna expandir para preencher espaço
                ),
                expand=True,
                alignment=ft.alignment.center  # Centraliza o container na tela
            )
        )
        page.update()  # Atualiza a página para refletir as mudanças

    # Função chamada ao selecionar um tema, guarda o tema escolhido e mostra tela para digitar nome
    def selecionar_tema(tema):
        nonlocal tema_selecionado
        tema_selecionado = tema
        mostrar_tela_nome()

    # Tela para o jogador digitar seu nome antes de iniciar o quiz
    def mostrar_tela_nome(e=None):
        page.controls.clear()
        page.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        botao_voltar(),  # Botão para voltar para escolha de tema
                        ft.Text("Digite seu nome para começar o quiz:", size=22, height=50, weight=ft.FontWeight.W_500),
                        nome_input,  # Campo de input para nome
                        iniciar_btn  # Botão para iniciar o quiz
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                expand=True,
                alignment=ft.alignment.center,
            )
        )
        page.update()

    # Tela que exibe a pergunta atual e as alternativas
    def mostrar_pergunta(e=None):
        page.controls.clear()

        # Se o quiz terminou, salva resultado e mostra tela de resultado
        if controller.quiz_finalizado():
            salvar_resultado()
            mostrar_resultado()
            return

        pergunta = controller.obter_pergunta_atual()  # Pega a pergunta atual do controlador
        alternativa_buttons = []  # Lista para guardar botões das alternativas para manipular depois

        # Função async para esperar 2 segundos e mostrar próxima pergunta
        async def esperar_e_mostrar():
            await asyncio.sleep(2)
            mostrar_pergunta()

        # Função chamada quando o jogador responde uma alternativa
        def responder(indice):
            correta = pergunta.correta  # índice da alternativa correta
            controller.responder(indice)  # registra resposta no controlador

            # Atualiza cores dos botões para indicar correta e errada
            for i, btn in enumerate(alternativa_buttons):
                if i == correta:
                    btn.bgcolor = ft.Colors.GREEN
                    btn.color = ft.Colors.WHITE
                elif i == indice:
                    btn.bgcolor = ft.Colors.RED
                    btn.color = ft.Colors.WHITE
                btn.disabled = True  # desabilita os botões para evitar múltiplos cliques
            page.update()

            # Após resposta, espera 2s e carrega próxima pergunta
            page.run_task(esperar_e_mostrar)

        # Função para criar um botão para cada alternativa, vinculando o índice para resposta
        def criar_botao_alternativa(texto, indice):
            btn = ft.ElevatedButton(
                text=texto,
                bgcolor=ft.Colors.WHITE,
                color="#57689e",
                width=400,
                height=40,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
                    shape=ft.RoundedRectangleBorder(radius=15),
                    padding=6)
            )
            btn.on_click = lambda e: responder(indice)
            alternativa_buttons.append(btn)
            return btn

        conteudo = ft.Column(
            [
                botao_voltar(),  # Botão para voltar
                ft.Text(pergunta.texto, size=25, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER, height=60),
            ] + [
                criar_botao_alternativa(alt, i) for i, alt in enumerate(pergunta.alternativas)  # Cria botões para todas alternativas
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        page.controls.append(
            ft.Container(
                content=conteudo,
                expand=True,
                alignment=ft.alignment.center
            )
        )

        page.update()

    # Tela que mostra a pontuação final e histórico de resultados
    def mostrar_resultado():
        page.controls.clear()

        # Campo para filtro por nome ou tema, inicialmente oculto
        filtro_input = ft.TextField(
            label="Filtrar por nome ou tema",
            width=300,
            visible=False,
            on_change=lambda e: atualizar_historico(filtro_input.value),  # Atualiza o histórico conforme digita
            on_blur=lambda e: esconder_filtro()  # Esconde o filtro quando perde foco
        )

        historico_container = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.ALWAYS  # Permite scroll sempre
        )

        historico_area = ft.Container(
            content=historico_container,
            width=500,
            height=200,
            bgcolor="#ffffff",
            border_radius=10,
            padding=10
        )

        # Atualiza lista de resultados filtrando por texto no filtro (nome ou tema)
        def atualizar_historico(filtro=""):
            historico_container.controls.clear()
            filtro_lower = filtro.lower()
            for nome, tema, pontuacao in reversed(carregar_resultados()):
                # Adiciona ao histórico se filtro bate com nome ou tema
                if filtro_lower in nome.lower() or filtro_lower in tema.lower():
                    historico_container.controls.append(
                        ft.Text(f"{nome} - Tema: {tema} - Acertos: {pontuacao}")
                    )
            if not historico_container.controls:
                historico_container.controls.append(ft.Text("Nenhum resultado encontrado."))
            page.update()

        # Mostra o campo de filtro quando ícone de lupa é clicado
        def mostrar_input_filtro(e):
            filtro_input.visible = True
            lupa_btn.visible = False
            page.update()
            filtro_input.focus()

        # Esconde o campo de filtro e reseta valor
        def esconder_filtro():
            filtro_input.visible = False
            lupa_btn.visible = True
            filtro_input.value = ""
            atualizar_historico()
            page.update()

        lupa_btn = ft.IconButton(
            icon=ft.Icons.SEARCH,
            tooltip="Mostrar filtro",
            on_click=mostrar_input_filtro
        )

        # Layout principal da tela de resultado
        page.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        botao_voltar(),
                        ft.Text(f"Pontuação: {jogador.pontuacao}", 
                                size=35,                                
                                weight=ft.FontWeight.W_700,
                                height=65,
                                ),
                        ft.Container(
                            width=500,
                            content=ft.Row(
                                [
                                    ft.Text("🏅 Históricos anteriores:", size=18, weight="bold", expand=True),
                                    lupa_btn,
                                    filtro_input
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ),
                        ft.Row([historico_area], alignment=ft.MainAxisAlignment.CENTER),
                        ft.ElevatedButton(text="Jogar novamente", 
                                        on_click=mostrar_tela_inicial,
                                        bgcolor="#052659,0.6",
                                        color="#ffffff",
                                        width=180,
                                        height=47,
                                        style=ft.ButtonStyle(
                                            text_style=ft.TextStyle(size=17, weight=ft.FontWeight.W_500),
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                            padding=20
                                        )
                                          ),
                    ],
                    spacing=20,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                expand=True,
                alignment=ft.alignment.center,
            )
        )

        atualizar_historico()  # Carrega histórico inicial sem filtro
        page.update()

    # Função chamada ao clicar no botão iniciar
    def iniciar_quiz(e):
        nonlocal controller
        jogador.nome = nome_input.value.strip()  # Remove espaços em branco do nome

        if not jogador.nome:  # Valida se o nome foi preenchido
            page.snack_bar = ft.SnackBar(ft.Text("Digite um nome!"))
            page.snack_bar.open = True
            page.update()
            return

        todas_perguntas = questoes_por_tema[tema_selecionado]  # Pega todas perguntas do tema escolhido
        perguntas_sorteadas = random.sample(todas_perguntas, 5)  # Sorteia 5 perguntas aleatórias
        controller = QuizController(perguntas=perguntas_sorteadas, jogador=jogador)  # Cria controlador do quiz
        controller.reiniciar()  # Reinicia o quiz para começar do zero

        mostrar_pergunta()  # Exibe a primeira pergunta

    # Função para salvar resultado do jogador no arquivo CSV
    def salvar_resultado():
        try:
            with open("resultados.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow([jogador.nome, tema_selecionado, jogador.pontuacao])
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")

    # Função para carregar resultados salvos no arquivo CSV
    def carregar_resultados():
        resultados = []
        try:
            with open("resultados.csv", "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.reader(arquivo)
                for linha in leitor:
                    if len(linha) == 3:
                        nome, tema, pontos = linha
                        resultados.append((nome, tema, pontos))
        except FileNotFoundError:
            pass  # Se o arquivo não existir, retorna lista vazia
        return resultados

    iniciar_btn.on_click = iniciar_quiz  # Associa evento de clique ao botão iniciar
    mostrar_tela_inicial()  # Mostra a tela inicial ao abrir o app

ft.app(target=main)  # Inicia o app Flet chamando a função main