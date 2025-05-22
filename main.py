import flet as ft
import csv
import random
import asyncio
from quiz_controller import QuizController
from jogador import Jogador
from questoes import questoes_por_tema

def main(page: ft.Page):
    page.title = "Quiz em Flet"
    page.window_width = 600
    page.window_height = 500
    page.bgcolor="#ccdceb"

    jogador = Jogador(nome="")
    controller = None
    tema_selecionado = None

    nome_input = ft.TextField(
        label="Digite seu nome",
        width=300,
        bgcolor="#5483b3,0.2",
        height=70,
        color="#ffffff",
        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_400)
    )

    iniciar_btn = ft.ElevatedButton(
        text="Iniciar Quiz",
        bgcolor="#052659,0.6",
        color="#ffffff",
        width=150,
        height=50,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=20, weight=ft.FontWeight.W_500),
            shape=ft.RoundedRectangleBorder(radius=20),
            padding=20
        )
    )

    def botao_voltar():
        return ft.IconButton(
            icon=ft.Icons.HOME,
            icon_size=40,
            height=50,
            icon_color="#052659,0.7",
            tooltip="Voltar para a página inicial",
            on_click=lambda e: mostrar_tela_inicial()
        )

    def mostrar_tela_inicial(e=None):
        page.controls.clear()
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
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                expand=True,
                alignment=ft.alignment.center
            )
        )
        page.update()

    def selecionar_tema(tema):
        nonlocal tema_selecionado
        tema_selecionado = tema
        mostrar_tela_nome()

    def mostrar_tela_nome(e=None):
        page.controls.clear()
        page.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        botao_voltar(),
                        ft.Text("Digite seu nome para começar o quiz:", size=22, height=50, weight=ft.FontWeight.W_500),
                        nome_input,
                        iniciar_btn
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

    def mostrar_pergunta(e=None):
        page.controls.clear()

        if controller.quiz_finalizado():
            salvar_resultado()
            mostrar_resultado()
            return

        pergunta = controller.obter_pergunta_atual()
        alternativa_buttons = []

        async def esperar_e_mostrar():
            await asyncio.sleep(2)
            mostrar_pergunta()

        def responder(indice):
            correta = pergunta.correta
            controller.responder(indice)

            for i, btn in enumerate(alternativa_buttons):
                if i == correta:
                    btn.bgcolor = ft.Colors.GREEN
                    btn.color = ft.Colors.WHITE
                elif i == indice:
                    btn.bgcolor = ft.Colors.RED
                    btn.color = ft.Colors.WHITE
                btn.disabled = True
            page.update()

            page.run_task(esperar_e_mostrar)

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
                botao_voltar(),
                ft.Text(pergunta.texto, size=25, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER, height=60),
            ] + [
                criar_botao_alternativa(alt, i) for i, alt in enumerate(pergunta.alternativas)
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

    def mostrar_resultado():
        page.controls.clear()

        filtro_input = ft.TextField(
            label="Filtrar por nome ou tema",
            width=300,
            visible=False,
            on_change=lambda e: atualizar_historico(filtro_input.value),
            on_blur=lambda e: esconder_filtro()
        )

        historico_container = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.ALWAYS
        )

        historico_area = ft.Container(
            content=historico_container,
            width=500,
            height=200,
            bgcolor="#ffffff",
            border_radius=10,
            padding=10
        )

        def atualizar_historico(filtro=""):
            historico_container.controls.clear()
            filtro_lower = filtro.lower()
            for nome, tema, pontuacao in reversed(carregar_resultados()):
                if filtro_lower in nome.lower() or filtro_lower in tema.lower():
                    historico_container.controls.append(
                        ft.Text(f"{nome} - Tema: {tema} - Acertos: {pontuacao}",)
                    )
            if not historico_container.controls:
                historico_container.controls.append(ft.Text("Nenhum resultado encontrado."))
            page.update()

        def mostrar_input_filtro(e):
            filtro_input.visible = True
            lupa_btn.visible = False
            page.update()
            filtro_input.focus()

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

        page.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        botao_voltar(),
                        ft.Text(f"Pontuação: {jogador.pontuacao}", size=22, color="green"),
                        ft.Text("🏅 Históricos anteriores:", size=18, weight="bold"),
                        ft.Row([lupa_btn, filtro_input], alignment=ft.MainAxisAlignment.START),
                        historico_area,
                        ft.ElevatedButton(text="Jogar novamente", on_click=mostrar_tela_inicial),
                    ],
                    spacing=20,
                    expand=True,
                ),
                expand=True,
                alignment=ft.alignment.center,
            )
        )

        atualizar_historico()
        page.update()

    def iniciar_quiz(e):
        nonlocal controller
        jogador.nome = nome_input.value.strip()

        if not jogador.nome:
            page.snack_bar = ft.SnackBar(ft.Text("Digite um nome!"))
            page.snack_bar.open = True
            page.update()
            return

        todas_perguntas = questoes_por_tema[tema_selecionado]
        perguntas_sorteadas = random.sample(todas_perguntas, 1)
        controller = QuizController(perguntas=perguntas_sorteadas, jogador=jogador)
        controller.reiniciar()

        mostrar_pergunta()

    def salvar_resultado():
        try:
            with open("resultados.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow([jogador.nome, tema_selecionado, jogador.pontuacao])
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")

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
            pass
        return resultados

    iniciar_btn.on_click = iniciar_quiz
    mostrar_tela_inicial()

ft.app(target=main)
