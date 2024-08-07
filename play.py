from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from main import app, games, Game

GAME_DURATION = 120 

# Generate a math problem
def generate_problem():

    # Determine the operator for the problem
    global GAME_MODE
    if GAME_MODE == "All":
        op = choice(["Add", "Sub", "Mul", "Div"])
    else:
        op = GAME_MODE

    # Generate n1 and n2
    if op in ["Add", "Sub"]:
        n1 = randint(2, 100)
        n2 = randint(2, 100)
    else:
        n1 = randint(2, 12)
        n2 = randint(2, 100)

    # Addition problem
    match op:
        case "Add":
            symbol = "+"
            func = lambda n1, n2 : n1 + n2
        case "Sub":
            n1 = n1 + n2
            symbol = "-"
            func = lambda n1, n2 : n1 - n2
        case "Mul":
            symbol = "×"
            func = lambda n1, n2 : n1 * n2
        case "Div":
            n1, n2 = n1 * n2, n1
            symbol = "÷"
            func = lambda n1, n2 : n1 // n2

    return n1, n2, symbol, func

def make_input():
    return Input(
        id="title", 
        name="ans", 
        hx_swap_oob="true",
        autofocus="true",
        autocomplete="off"
    )

def make_question():
    global question
    n1, n2, symbol, func = question
    return H3(f"{n1} {symbol} {n2}", id="question", hx_swap_oob="true")

@app.get("/play")
def play(game_mode: str):
    global score
    global question
    global time
    global GAME_MODE

    score = 0
    time = GAME_DURATION
    GAME_MODE = game_mode
    question = generate_problem()

    return Title("Zetamac Reloaded - Play"), Main(
        P(
            f"Time: {GAME_DURATION}", 
            hx_get = "/countdown",
            hx_trigger = "every 1s",
            hx_swap = "innerHTML",
            hx_swap_oob = "true",
            id = "timer"
        ),
        P("Score: 0", id="score"),
        make_question(),
        Form(
            Group(make_input()),
            hx_post = "/submit-answer", 
            hx_target = "#score", 
            hx_swap = "innerHTML",
            hx_trigger = "keyup",
            id = "game-input"
        ), Br(),
        Form(
            Button(
                "Quit", 
                formaction="/",  
                hx_swap_oob="true",
                id = "exit-button"
            )
        ),
        Div(
            hx_swap_oob = "true",
            id = "submit-menu"
        )
    )


@app.post("/submit-answer")
def submit(ans : str):

    global score
    global question
    global time
    global GAME_MODE

    n1, n2, symbol, func = question

    if ans.isnumeric() and int(ans) == func(n1, n2) and time > 0:
        score += 1
        question = generate_problem()
        return f"Score: {score}", make_question(), make_input()

    return f"Score: {score}"

@app.get("/countdown")
def countdown():

    global time
    global score
    global GAME_MODE

    # Update the countdown
    if time > 0:
        time -= 1
        return f"Time: {time}"

    # Stop the timer
    timer = P("Time: 0", hx_swap_oob = "true", id = "timer")

    # Get the data at which the game was played
    date_played = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Replace the quit button with a finish button
    finish_button = Button(
        "Finish",
        formaction = "/",
        hx_swap_oob = "true",
        id = "exit-button"
    )

    # Add a menu to submit your score
    submit_form = Form(
        Input(type = "hidden", name = "date", value = date_played),
        Input(type = "hidden", name = "score", value = score),
        Label("Initials: ",
            Input(id = "initials-input", name = "initials", maxlength = 3),
            Button("Submit Score", id="submit-button", type="submit")
        ),
        hx_post = "/submit-score",
        hx_target = "#submit-button",
        hx_swap = "outerHTML",
    )

    submit_menu = Div(
        Br(), Hr(), Br(),
        submit_form,
        hx_swap_oob = "true",
        id = "submit-menu"
    )

    return f"Time: 0", timer, finish_button, submit_menu

@app.post("/submit-score")
def submit_score(session, date: str, score: int, initials: str):


    # Add game to local scores, stored in sessions
    global GAME_MODE
    session.setdefault(GAME_MODE, [])
    session[GAME_MODE].append({
        "initials": initials,
        "date": date,
        "score": score
    })

    # Add game to global score database
    games.insert(Game(
        date=date, 
        score=score, 
        gm=GAME_MODE, 
        initials=initials
    ))

    return Button("Submitted!", id="submit-button", disabled="true") 
