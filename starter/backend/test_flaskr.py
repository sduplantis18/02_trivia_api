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
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
        res = self.client().get('/categories/16')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_get_questions_failure(self):
        res = self.Client().get('/questions')
        data = json.loads(res.data)


    def test_delete_question(self):
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        
        question = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success', True])
        self.assertEqual(data['deleted'], str(question_id))
        self.assertEqual(question, None)

    def test_add_question(self):
        test_data = {
            'question' = "Test question",
            'answer' = "Test answer",
            'difficulty' = 1,
            'category' = 2
        }
        response.self.client().post('/questions', json=test_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()