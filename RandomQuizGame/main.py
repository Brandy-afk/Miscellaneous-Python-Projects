import requests as rq
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface


def get_questions():
    response = rq.get('https://opentdb.com/api.php?amount=20&category=15&difficulty=medium&type=boolean')
    response.raise_for_status()
    questions = [Question(question_text=question['question'], answer=question['correct_answer'])
                 for question in dict(response.json())['results']]
    return questions


brain = QuizBrain(get_questions())
interface = QuizInterface(brain)

