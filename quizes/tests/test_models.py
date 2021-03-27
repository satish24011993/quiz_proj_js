from django.test import TestCase
from quizes.models import Quiz

class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(name="Django Quiz",topic="multi-tenent", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
        Quiz.objects.create(name="Programming Quiz", topic="Data Structures", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
    
    def test_quiz_topic(self):
        """Identifing the topics of quizes"""
        django_quiz = Quiz.objects.get(name="Django Quiz")
        programming_quiz = Quiz.objects.get(name="Programming Quiz")
        self.assertEqual(str(django_quiz.topic), "multi-tenent")
        self.assertEqual(str(programming_quiz.topic), "Data Structures")

    def test_quiz_no_of_questions(self):
        "Checking no of questions"
        django_quiz = Quiz.objects.get(name="Django Quiz")
        programming_quiz = Quiz.objects.get(name="Programming Quiz")
        self.assertEqual(django_quiz.number_of_questions, 2)
        self.assertEqual(programming_quiz.number_of_questions, 2)

    def test_quiz_time(self):
        "Checking time"
        django_quiz = Quiz.objects.get(name="Django Quiz")
        programming_quiz = Quiz.objects.get(name="Programming Quiz")
        self.assertEqual(django_quiz.time, 10)
        self.assertEqual(programming_quiz.time, 10)

    def test_quiz_required_score_to_pass(self):
        "Checking required score"
        django_quiz = Quiz.objects.get(name="Django Quiz")
        programming_quiz = Quiz.objects.get(name="Programming Quiz")
        self.assertEqual(django_quiz.required_score_to_pass, 50)
        self.assertEqual(programming_quiz.required_score_to_pass, 50)

    def test_quiz_difficulty(self):
        "Checking Quiz difficulty"
        django_quiz = Quiz.objects.get(name="Django Quiz")
        programming_quiz = Quiz.objects.get(name="Programming Quiz")
        self.assertEqual(int(django_quiz.difficulty), 1)
        self.assertEqual(int(programming_quiz.difficulty), 1)