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
    
    def test_process_guess(self):
        with app.test_client() as client:
            res = client.post('/guess', data = {'playerGuess' : 'saw'})
            html = res.get_data(as_text=True)


            self.assertEqual(res.status_code, 400)
            

    def test_update_score(self):
        with app.test_client() as client:
            pass

    def test_final_score(self):
        with app.test_client() as client:
            res = client.get('/score')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            