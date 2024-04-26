from tkinter import *
from quiz_brain import QuizBrain
class QuizInterface:
    BACKGROUND_COLOR = "#496989"
    CORRECT_COLOR = "#A8CD9F"
    WRONG_COLOR = "#A0153E"

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(pady=30, padx=30, background=QuizInterface.BACKGROUND_COLOR)
        self.score_label = Label(text="Score: 0", font=("Ariel", 14), fg='white', bg=QuizInterface.BACKGROUND_COLOR)
        self.score_label.grid(row=0, column=1, sticky='e')

        self.board_canvas = Canvas(width=350, height=400, background='white')
        self.board_canvas.grid(row=1, column=0,columnspan=2, pady=20)
        self.question_text = self.board_canvas.create_text(175,200, width=250, text="Whats 2+2?",
                                                           font=("Ariel", 24), fill=QuizInterface.BACKGROUND_COLOR,
                                                           justify=CENTER, anchor=CENTER)

        self.false_image = PhotoImage(file="images/false.png")
        self.true_image = PhotoImage(file="images/true.png")

        self.true_button = Button(image=self.true_image, width=100, height=100,highlightthickness=0,
                                  command=self.on_true_pressed)
        self.true_button.grid(row=2, column=0)
        self.false_button = Button(image=self.false_image, width=100, height=100,highlightthickness=0,
                                   command=self.on_false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_questions():
            question = self.quiz.next_question()
            self.board_canvas.itemconfig(self.question_text, text=question.question_text)
        else:
            self.on_game_over()

    def on_true_pressed(self):
        self.check_response('True')

    def on_false_pressed(self):
        self.check_response('False')

    def check_response(self, answer):
        if self.quiz.check_answer(answer):
            self.score_label.config(text=f"Score: {self.quiz.score}")
        self.get_next_question()

    def on_game_over(self):
        self.board_canvas.itemconfig(self.question_text, text=f"{self.quiz.score}/{len(self.quiz.questions)}\n"
                                                              f"Game Over")
        self.true_button.grid_remove()
        self.false_button.grid_remove()
        self.score_label.grid_remove()


