from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from main import app, games, Game, render

@app.post("/update_global")
def update_global(game_mode: str):
    games.xtra(gm=game_mode)
    return Table(
        Tr(Th("Player"), Th("Date"), Th("Score")), 
        *games(limit = 10, order_by = "score DESC"),
        id="games-list"
    )

@app.get("/global_leaderboard")
def global_leaderboard():
    games.xtra(gm="All")
    return Title("Zetamac Reloaded - Global Leaderboard"), Main(
        H3("Global High Scores"),
        Form(
            Select(
                Option("All Operations", value = "All", selected=""),
                Option("Addition Only", value = "Add"),
                Option("Subtraction Only", value = "Sub"),
                Option("Multiplication Only", value = "Mul"),
                Option("Division Only", value = "Div"),
                name = "game_mode",
                autocomplete = "off",
                hx_post = "/update_global",
                hx_target = "#games-list",
                hx_swap = "outerHTML"
            ),
        ),
        Hr(),
        Table(
            Tr(Th("Player"), Th("Date"), Th("Score")),
            *games(limit = 10, order_by = "score DESC"), 
            id="games-list"
        ),
        Hr(),
        Form(Button("Back", formaction="/"))
    )

# Returns the top 10 scores stored locally
def get_scores(data):

    data = sorted(data, key = lambda d : d["score"], reverse = True)
    data = data[:10]
    rows = []

    for d in data:
        initials, date, score = d.values()
        rows.append(Tr(Td(initials), Td(date), Td(score)))

    return (data, rows)


@app.post("/update_local")
def update_local(session, game_mode: str):

    # Overwrite the session data to ensure no more than 10 entries are kept
    session.setdefault(game_mode, [])
    data, rows = get_scores(session[game_mode])
    session[game_mode] = data

    return Table(
        Tr(Th("Player"), Th("Date"), Th("Score")),
        *rows,
        id="local-games-list"
    )

@app.get("/local_leaderboard")
def local_leaderboard(session):

    session.setdefault("All", [])
    return Title("Zetamac Reloaded - Local Leaderboard"), Main(
        H3("Local High Scores"),
        Form(
            Select(
                Option("All Operations", value = "All", selected=""),
                Option("Addition Only", value = "Add"),
                Option("Subtraction Only", value = "Sub"),
                Option("Multiplication Only", value = "Mul"),
                Option("Division Only", value = "Div"),
                name = "game_mode",
                autocomplete = "off",
                hx_post = "/update_local",
                hx_target = "#local-games-list",
                hx_swap = "outerHTML"
            ),
        ),
        Hr(),
        Table(
            Tr(Th("Player"), Th("Date"), Th("Score")),
            *get_scores(session["All"])[-1], 
            id="local-games-list"
        ),
        Hr(),
        Form(Button("Back", formaction="/"))
    )
