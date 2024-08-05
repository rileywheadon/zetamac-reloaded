from fasthtml import FastHTML
from fasthtml.common import *

def render(game):
    return Tr(Td(f"{game.id}"), Td(f"{game.score}"))

# Load the database from mathapp.db, create a "games" table if necessary
app, rt, games, Game = fast_app(
    'data/mathapp.db', 
    render = render,
    id = str, 
    score = int, 
    mode = str, 
    pk = 'id',
    hdrs = (
        picolink, 
        Link(rel="stylesheet", href="style.css", type="text/css")
    )
)

from home import *
from play import *
from stats import *

