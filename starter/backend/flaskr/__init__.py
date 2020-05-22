import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1,type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={'/':{'origins':"*"}})
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  ''' 
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'Get, Post, Patch, Delete, Options')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_category = [category.format() for category in categories]
    return jsonify({
      'success':True,
      'categories':formatted_category
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    #get questions
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    
    #get category list
    categories = Category.query.all()
    category_list = {}
    for category in categories:
      category_list[category.id] = category.type

    return jsonify({
      'success':True,
      'questions':current_questions,
      'categories': category_list,
      'totalQuestions':len(Question.query.all()),
      'current_category': None
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      #get question by id
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      #delete the question
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success':True,
        'deleted':question_id,
        'questions':current_questions
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    
    body = request.get_json()
    
    new_question = body.get('question', None)
    new_answer_text = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty_score = body.get('difficulty', None)

    try:
      question = Question(question=new_question,answer=new_answer_text,category=new_category,difficulty=new_difficulty_score)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success':True,
        'created':Question.id,
        'questions':current_questions,
        'total questions':len(Question.query.all())
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    try:
      #define search term
      body = request.get_json()
      search_term = body.get('search_term','')
      #filter questions by search term
      result = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
      #format questions
      formatted_questions = [question.format() for question in result]
      return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions':len(result),
        'current_category':None
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      questions = Question.query.filter_by(category=str(category_id)).all()
      formatted_questions = paginate_questions(request, questions)
      return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions':len(Question.query.all()),
        'current_category':category.type
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      #setup request body
      body = request.get_json()
      #get quizz categories
      category = body.get("quiz_category")
      #get previous question
      previous_questions = body.get('previous_questions')
      
      #get all questions if ALL is selected
      if category["id"] == 0:
        questions = Question.query.all()
      #load questions for specific category  
      else:
        questions = Question.query.filter_by(category = category["id"]).all()
      #select random question from questions
      def random_question():
          return questions[random.randrange(0, len(questions), 1)]
      new_question = random_question()

      #check if new quetsion has been used already
      found = True
      while found:
        if new_question.id in previous_questions:
          new_question = random_question()
        else:
          found = False

      return jsonify({
        'success':True,
        'question':new_question.fomat()
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  #404 error handler
  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':"Not Found"
    })
  #422 error handler
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':"Unable to process the request"
    })
  
  return app

    