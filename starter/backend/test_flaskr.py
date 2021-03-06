import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = f'postgresql://sdupl:Baller24@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'])
        self.assertEqual(len(data['questions']))
        self.assertEqual(len(data['categories']))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_category_without_result(self):
        #tested with invalid category
        category_id = 1000
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_get_questions_failure(self):
        #tested with invalid page number
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Not Found')

    def test_delete_question(self):
        #Test with hardcoded question id that exists in the db. 
        question_id = 12
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'], 12)
    
    def test_delete_question_fail(self):
        #test with invalid question id
        question_id = 5000
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Unable to process the request')

    def test_add_question(self):
        test_data = {
            'question' : 'New Question',
            'answer' : 'New Answer',
            'difficulty' : 1,
            'category' : 2
        }
        res = self.client().post('/questions', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        

    def test_add_question_fail(self):
        #fail when attemping to post new question with empty json
        test_data = {}
        res = self.client().post('/questions/', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_pass_get_quiz_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client().post('/quizzes', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'],
                             request_data['previous_questions'])

    def test_fail_get_questions_for_quiz(self):
        #no post data supplied
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_search_question(self):
        search_term = {'search_term':'test'}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def fail_search_question(self):
        search_term = {'search_term':''}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()