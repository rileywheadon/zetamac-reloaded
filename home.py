from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from app import app, games, Game

# Update the settings object
@app.post("/update_settings")
def update_settings(session, game_mode: str):
    session["mode"] = game_mode

@app.get("/")
def home(session):
    return Title("Zetamac Reloaded"), Main(
        H1("Zetamac Reloaded"),
        P("This is an updated version of", A("Zetamac", href="https://arithmetic.zetamac.com/"), "which allows you to keep track of your scores. As of now, only a limited number of game modes are available. If you're interested, my other projects and contact information are located", A("here", href="https://rwheadon.dev")," on my blog.", id="about-text"),
        H3("Game Mode"),
        Form(get_options(session)),
        Br(),
        Form(Div(
            Button("Stats", formaction="/statistics"),
            Button("Play", formaction="/play")
        ))
    )

def get_options(session):

    options = {
        "All Operations": "All",
        "Addition Only": "Add",
        "Subtraction Only": "Sub",
        "Multiplication Only": "Mul",
        "Division Only": "Div"
    }
    
    selectors = []
    for key, val in options.items():
        kwa = {"value": val}
        if session["mode"] == val: kwa["selected"] = "selected"
        selectors.append(Option(key, **kwa))

    return Select(*selectors, name="game_mode", 
                  hx_post="update_settings", hx_swap="none")
