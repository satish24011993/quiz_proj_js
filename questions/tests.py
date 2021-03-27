from django.test import TestCase
from questions.models import Answer, Question
from quizes.models import Quiz


class QuestionsTestCase(TestCase):
    def setUp(self):
        quiz1 = Quiz.objects.create(name="Django Quiz",topic="multi-tenent", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
        quiz2 = Quiz.objects.create(name="Programming Quiz", topic="Data Structures", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
        Question.objects.create(text="Is Django backend framework?", quiz=quiz1)
        Question.objects.create(text="What does manage.py does in django?", quiz=quiz2)

    def test_question_text(self):
        """Identifing the text of question"""
        question_1 = Question.objects.get(text="Is Django backend framework?")
        question_2 = Question.objects.get(text="What does manage.py does in django?")
        self.assertEqual(str(question_1.text), "Is Django backend framework?")
        self.assertEqual(str(question_2.text), "What does manage.py does in django?")

class AnswerTestCase(TestCase):
    def setUp(self):
        quiz1 = Quiz.objects.create(name="Django Quiz",topic="multi-tenent", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
        question_1 = Question.objects.create(text="Is Django backend framework?", quiz=quiz1)
        Answer.objects.create(text="Yes", correct= True, question=question_1)
        Answer.objects.create(text="No", correct= False,question=question_1)

    def test_answer_text(self):
        ans_1 = Answer.objects.get(text="Yes")
        ans_2 = Answer.objects.get(text="No")
        self.assertEqual(str(ans_1.text), "Yes")
        self.assertTrue(ans_1.correct)
    
    def test_correct_answer(self):
        ans_1 = Answer.objects.get(text="Yes")
        ans_2 = Answer.objects.get(text="No")
        self.assertTrue(ans_1.correct)
        self.assertFalse(ans_1.correct == False)
