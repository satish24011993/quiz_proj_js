from django.test import TestCase
from quizes.models import Quiz
from questions.models import Question, Answer
from results.models import Result
from django.contrib.auth.models import User
# Create your tests here.

class ResultTestCase(TestCase):
    def setUp(self):
        quiz1 = Quiz.objects.create(name="Django Quiz",topic="multi-tenent", number_of_questions=2, time=10, required_score_to_pass=50, difficulty=1)
        user1 = User.objects.create(username="testuser", password="testpassword")
        Result.objects.create(quiz=quiz1, user=user1, score=80.00)
    
    def test_result_score(self):
        result_1 = Result.objects.get(score=80.00)
        self.assertEqual(result_1.score, 80.00)