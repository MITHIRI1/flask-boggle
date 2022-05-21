from flask import Flask, request, render_template, redirect, flash, jsonify, session
from boggle import Boggle

boggle_game = Boggle()


app = Flask(__name__)
app.config['SECRET_KEY'] = "its a secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

BOARD_KEY = "board"
HIGH_SCORE_KEY = "highscore"
NUM_PLAYS_KEY = "num_plays"


@app.route('/')
def home_board():
  
  
    board = session[BOARD_KEY]
    highscore = session.get(HIGH_SCORE_KEY, 0)
    num_plays = session.get(NUM_PLAYS_KEY, 0)

    return render_template('board.html', board=board, highscore=highscore, num_plays=num_plays)


@app.route('/new')
def create_board():
  
    board = boggle_game.make_board()

    
    num_plays = session.get(NUM_PLAYS_KEY, 0)
    session[NUM_PLAYS_KEY] = num_plays + 1

   
    session[BOARD_KEY] = board

   
    return redirect('/')


@app.route('/check-guess')
def check_guess():

    
    word = request.args['word']
    board = session[BOARD_KEY]
    result = boggle_game.check_valid_word(board, word)
  
    return jsonify({"result": result})


@app.route('/post-score', methods=["POST"])
def post_score():

    score = request.json['score']

    highscore = session.get(HIGH_SCORE_KEY, 0)
    num_plays = session.get(NUM_PLAYS_KEY, 0)

    broke_record = True if score > highscore else False

    session[HIGH_SCORE_KEY] = max(score, highscore)
    session[NUM_PLAYS_KEY] = num_plays + 1

    return jsonify( highscore=session[HIGH_SCORE_KEY], broke_record=broke_record)