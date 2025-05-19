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

    jogador = Jogador(nome="")
    controller = None
    tema_selecionado = None

    nome_input = ft.TextField(label="Digite seu nome", width=300)
    iniciar_btn = ft.ElevatedButton(text="Iniciar Quiz")

    def botao_voltar():
        return ft.IconButton(
            icon=ft.Icons.HOME,
            tooltip="Voltar para a página inicial",
            on_click=lambda e: mostrar_tela_inicial()
        )

    def mostrar_tela_inicial(e=None):
        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    ft.Text("🎮 Bem-vindo ao Super Quiz!", size=28, weight="bold", color="purple"),
                    ft.Text("Escolha um tema para começar:", size=18),
                    ft.ElevatedButton(text="Curiosidades Gerais", on_click=lambda e: selecionar_tema("curiosidades")),
                    ft.ElevatedButton(text="Música", on_click=lambda e: selecionar_tema("musica")),
                    ft.ElevatedButton(text="Pegadinhas e Lógica", on_click=lambda e: selecionar_tema("logica")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
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
            ft.Column(
                [
                    botao_voltar(),
                    ft.Text("Digite seu nome para começar o quiz:", size=22),
                    nome_input,
                    iniciar_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
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
        page.controls.append(botao_voltar())
        page.controls.append(ft.Text(pergunta.texto, size=20, weight="bold"))

        alternativa_buttons = []

        async def esperar_e_mostrar():
            await asyncio.sleep(2)
            mostrar_pergunta()

        def responder(indice):
            correta = pergunta.correta
            controller.responder(indice)

            # Muda cores dos botões
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

        for i, alt in enumerate(pergunta.alternativas):
            btn = ft.ElevatedButton(text=alt, width=500)
            btn.on_click = lambda e, idx=i: responder(idx)
            alternativa_buttons.append(btn)
            page.controls.append(btn)

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

        historico_container = ft.Column(spacing=5, expand=True)

        def atualizar_historico(filtro=""):
            historico_container.controls.clear()
            filtro_lower = filtro.lower()
            for nome, tema, pontuacao in carregar_resultados():
                if filtro_lower in nome.lower() or filtro_lower in tema.lower():
                    historico_container.controls.append(
                        ft.Text(f"{nome} - Tema: {tema} - Acertos: {pontuacao}")
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
            ft.Column(
                [
                    botao_voltar(),
                    ft.Text(f"Pontuação: {jogador.pontuacao}", size=22, color="green"),
                    ft.Text("🏅 Históricos anteriores:", size=18, weight="bold"),
                    ft.Row([lupa_btn, filtro_input], alignment=ft.MainAxisAlignment.START),
                    historico_container,
                    ft.ElevatedButton(text="Jogar novamente", on_click=mostrar_tela_inicial),
                ],
                spacing=20,
                expand=True,
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
        perguntas_sorteadas = random.sample(todas_perguntas, 5)
        controller = QuizController(perguntas=perguntas_sorteadas, jogador=jogador)
        controller.reiniciar()

        mostrar_pergunta()

    def salvar_resultado():
        try:
            with open("resultados.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                # grava nome, tema e pontuação (acertos)
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
