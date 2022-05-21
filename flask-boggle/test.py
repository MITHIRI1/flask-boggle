from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


app.config['TESTING'] = True



class FlaskTests(TestCase):

    def setUp(self):
        
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        

        with self.client:
            response = self.client.get('/new')
            self.assertIn('board', session)
            self.assertIn('num_plays', session)
            self.assertIsNone(session.get('highscore'))
            self.assertEqual(response.status_code, 302)
            
        
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn('num_plays', session)
            self.assertIsNone(session.get('highscore'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'<div id="game">', response.data)
            self.assertIn(b'Score:', response.data)


    def test_valid_word(self):
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],]

            response = self.client.get('/check-guess?word=cat')
            self.assertEqual(response.json['result'], 'ok')
            self.assertEqual(response.status_code, 200)
    

    def test_invalid_word(self):
        
        self.client.get("/new")
        response = self.client.get('/check-guess?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')
        self.assertEqual(response.status_code, 200)


    def test_not_a_word(self):
        
        self.client.get("/new")
        response = self.client.get('/check-guess?word=dsafd')
        self.assertEqual(response.json['result'], 'not-word')
        self.assertEqual(response.status_code, 200)
