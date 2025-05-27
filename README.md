# Quiz com Flet

Este é um projeto de um **quiz interativo** desenvolvido com [Flet](https://flet.dev/), que permite ao usuário escolher temas, responder perguntas e visualizar seu histórico de pontuação!

## Funcionalidades:

- Escolha entre diferentes temas:
  - Curiosidades Gerais.
  - Música.
  - Pegadinhas e Lógica.
- Nome personalizado do jogador.
- Resposta com feedback visual (certa = verde, errada = vermelho).
- Pontuação final exibida após o quiz.
- Histórico de resultados salvos localmente em CSV.
- Filtro de histórico por nome ou tema.

## Tecnologias utilizadas:

- [Python 3.10+](https://www.python.org/)
- [Flet](https://flet.dev/) – para a interface gráfica (GUI).
- `csv` – para salvar e ler os resultados localmente.
- `asyncio`, `random` – para controlar eventos e aleatoriedade.
