from fasthtml import FastHTML
from fasthtml.common import *
from random import randint, choice
from datetime import datetime
from app import app, games, Game

# Generate a math problem
def generate_problem(session):

    # Determine the operator for the problem
    if session["mode"] == "All":
        op = choice(["Add", "Sub", "Mul", "Div"])
    else:
        op = session["mode"]

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
def play(session):

    global score
    global question
    global time

    score = 0
    time = 120
    question = generate_problem(session)

    return Title("Zetamac Reloaded - Play"), Main(
        P(
            "Time: 120", 
            hx_get = "/countdown",
            hx_trigger = "every 1s",
            hx_swap = "innerHTML",
        ),
        make_question(),
        Form(
            Group(make_input()),
            hx_post = "/submit-answer", 
            hx_target = "#score", 
            hx_swap = "innerHTML",
            hx_trigger = "keyup",
            id = "game-input"
        ),
        P("Score: 0", id="score"),
        Form(
            Button("Quit", formaction="/", id="exit", hx_swap_oob="true"), 
        ),
    )


@app.post("/submit-answer")
def submit(session, ans : str):

    global score
    global question
    global time

    n1, n2, symbol, func = question

    if ans.isnumeric() and int(ans) == func(n1, n2) and time > 0:
        score += 1
        question = generate_problem(session)
        return f"Score: {score}", make_question(), make_input()

    return f"Score: {score}"

@app.get("/countdown")
def countdown(session):

    global time
    global score

    # Update the countdown
    if time > 0:
        time -= 1
        return f"Time: {time}"

    # Add the game to the database, update the button
    elif time == 0:

        # Replace the finish button with an exit button
        exit_button = Button(
            "Finish", 
            id="exit", 
            formaction="/", 
            hx_swap_oob="true"
        )
        time -= 1

        # Save the game
        time_played = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        game = Game(time_played, score, session["mode"])
        games.insert(game)
        return f"Time: 0", exit_button

    # Do nothing, output time = 0
    else: return "Time: 0"

