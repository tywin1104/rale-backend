from .question_identifier import IsQuestion
from db.db import update_result
from .lda import LDA

class Dispatcher:
    def __init__(self):
        self.question_identifier = IsQuestion()
        self.lda = LDA()

    def update_result(self, record):
        new_question = self.identify_new_question_phrase(record)
        new_topic = self.identify_new_topic(record)
        update_result(new_topic, new_question)

    def identify_new_question_phrase(self, record):
        text, timestamp = record['text'], record['timestamp']
        is_question = True if self.question_identifier.predict_question() == 1 else False
        if is_question:
            question_type = self.question_identifier.predict_question_type()
            return [{"question": text, "question_type": question_type}]

        return []

    def identify_new_topic(self, record):
        text, timestamp = record['text'], record['timestamp']
        return self.lda.load_model(text)
