from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'S$cr3t12K3y'

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """Renders Game Home Page"""

    return render_template('home.html')


@app.route('/start/')
def play_game():
    """Renders the Game Board Page"""

    session["times_played"] = session.get('times_played', 0) +1
    board = boggle_game.make_board()
    session["board"] = board
    session['score'] = 0
    return render_template('game.html', board = board)


@app.route('/guess', methods = ["POST"])
def process_guess():
    """Processes and Validates User's Guess and Returns JSON"""

    guess = request.json.get('playerGuess')
    board = session['board']
    validate_guess = boggle_game.check_valid_word(board, guess.lower())

    if guess.lower() in boggle_game.words:
        if validate_guess == 'ok':
            return jsonify({"result": "ok"})

        elif validate_guess == "not-on-board":
            return jsonify({"result": "not-on-board"})

        else:
            return jsonify({"result": "not-a-word"})
    else:
        return jsonify({"result": "Not a Valid Word"})


@app.route('/update_score', methods = ["POST"])
def update_score():
    """Updates Score at the End of the Game"""

    score = request.json.get('score', 0)
    session["score"] = score
    return jsonify({"result":"Score Saved"})  


@app.route('/score')
def final_score():
    """Renders the Score Page with User's Statistics"""

    times_played = session["times_played"]
    score = session["score"]

    session["high_score"] = max(score, session.get("high_score", score))

    high_score = session["high_score"]
    
    return render_template('score.html', score=score, high_score = high_score, times_played = times_played)