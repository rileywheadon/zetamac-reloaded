from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from app import app, games, Game, render


@app.post("/update_statistics")
def update_statistics(game_mode: str):
    games.xtra(mode=game_mode)
    return Table(
        Tr(Th("Date"), Th("Score")),
        *games(limit = 10, order_by = "score DESC"),
        id="games-list"
    )

@app.get("/statistics")
def statistics():

    games.xtra(mode="All")
    return Title("Zetamac Reloaded - Stats"), Main(
        H3("High Scores"),
        Form(
            Select(
                Option("All Operations", value = "All", selected=""),
                Option("Addition Only", value = "Add"),
                Option("Subtraction Only", value = "Sub"),
                Option("Multiplication Only", value = "Mul"),
                Option("Division Only", value = "Div"),
                name = "game_mode",
                hx_post = "/update_statistics",
                hx_target = "#games-list",
                hx_swap = "outerHTML"
            ),
        ),
        Hr(),
        Table(
            Tr(Th("Date"), Th("Score")),
            *games(limit = 10, order_by = "score DESC"), 
            id="games-list"
        ),
        Hr(),
        Form(Button("Back", formaction="/"))
    )

