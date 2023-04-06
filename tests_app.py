from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            # self.assertEqual(res.status_code, 200)
            # self.assertIn('<button id="play-game">START GAME</button>', html)

    def test_time_played(self):
        with app.test_client() as client:
            res = client.get('/play_game')

            self.assertEqual(res.status_code, 200)

    def test_play_game(self):
        with app.test_client() as client:
            res = client.get('/play_game/')
            html = res.get_data(as_text=True)
            game = Boggle()
            board = game.make_board()
            session['board'] = board


            self.assertEqual(res.status_code, 200)
            
            self.assertEqual(session['times_played'], 1)
            self.assertIsNotNone(session['board'])
            self.assertEqual(session['score'], 0)

    
    def test_process_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                board = Boggle().make_board()
                session['board'] = board
        res = client.post('/guess', json={'playerGuess': 'srrww'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['result'], 'Not a Valid Word')


    def test_update_score(self):
        with app.test_client() as client:
          
            res = client.post('/update_score', json={'score': 3})

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json, {'result':'Score Saved'})
            self.assertEqual(session['score'], 3)


    
    def test_final_score(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['times_played'] = 1
                session['score'] = 1
                session['high_score'] = 0

        res = client.get('/score')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(f'<p id="final-score">1</p>', html)
        self.assertIn(f'<p id="high-score">1</p>', html)
        self.assertIn(f'<p>1 Times</p>', html)