from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from main import app, games, Game

# Get the home page
@app.get("/")
def home():

    # Reset the view of the games database
    games.xtra()

    # Return the home page
    return Title("Zetamac Reloaded"), Main(
        H1("Zetamac Reloaded"),
        P("This is an updated version of", A("Zetamac", href="https://arithmetic.zetamac.com/"), "with a global and local leaderboard. As of now, only a limited number of game modes are available. If you're interested, my other projects and contact information are located", A("here", href="https://rwheadon.dev")," on my blog.", id="about-text"), Br(),
        Form(
            Select(
                Option("All Operations", value="All"),
                Option("Addition Only", value="Add"),
                Option("Subtraction Only", value="Sub"),
                Option("Multiplication Only", value="Mul"),
                Option("Division Only", value="Div"),
                autocomplete = "off",
                name = "game_mode"
            ),
            Button("Play", formaction="/play")
        ), 
        H3("Leaderboards"),
        Form(
            Button("Global", formaction="/global_leaderboard"),
            Button("Local", formaction="/local_leaderboard"),
        )
    )

