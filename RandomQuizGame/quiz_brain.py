import html
from question_model import Question
class QuizBrain:
    def __init__(self, questions):
        self.questions = questions
        self.question_number = 0
        self.score = 0
        self.current_question = None

    def still_questions(self):
        return self.question_number < len(self.questions)

    def next_question(self) -> Question:
        self.current_question = self.questions[self.question_number]
        self.question_number += 1
        self.current_question.question_text = html.unescape(self.current_question.question_text)
        return self.current_question

    def check_answer(self, answer: str) -> bool:
        if self.current_question.correct_answer == answer:
            self.score += 1
            return True
        else:
            return False

