from boggle import Boggle
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'S$cr3t12K3y'

toolbar = DebugToolbarExtension(app)

