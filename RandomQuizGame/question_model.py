class Question:
    def __init__(self, **para):
        self.question_text = para['question_text']
        self.correct_answer = para['answer']
        return
