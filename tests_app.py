from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button id="start-game">START GAME</button>', html)

    def test_play_game(self):
        with app.test_client() as client:
            res = client.get('/start/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<td></td>', html)
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


    # def test_update_score(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             score = 1
    #             session['score'] = score
    #         res = client.post('/guess', json={'score': 3})

    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(res.json['result'], 'Score Saved')


    # def test_update_score(self):
    #     with app.test_client() as client:
            
    #         res = client.post('/update_score', data =({'score': '2'}))
    #         self.assertEqual(res.json, {'result':'Score Saved'})

    # def test_final_score(self):
    #     with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             session['times_played'] = 1
    #             session['score'] = 1
    #             session['high_score'] = 0
            
    #         res = client.get('/score')
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertEqual(session['high_score'], 1)
    