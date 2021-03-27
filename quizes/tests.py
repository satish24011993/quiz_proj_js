from django.test import TestCase
from quizes.models import Quiz
from django.test import RequestFactory
from questions.models import Answer, Question
from quizes.models import Quiz
from django.contrib.auth.models import User
from quizes import views
from django.http import Http404
from django.urls import resolve
from django.urls.exceptions import Resolver404

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


from django.test import TestCase, RequestFactory
from questions.models import Answer, Question
from quizes.models import Quiz
from django.contrib.auth.models import User
from quizes import views
from django.http import Http404
from django.urls import resolve
from django.urls.exceptions import Resolver404


class QuizListTest(TestCase):
    longMessage = True

    def test_environment_set_in_context(self):
        req = RequestFactory().get('/')
        req.user = User()
        resp = views.QuizListView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 200)


class ViewRequestFactoryTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True
    view_class = None

    def get_response(self, method):
        factory = RequestFactory()
        req = getattr(factory, method)('/')
        req.user = User()
        return self.view_class.as_view()(req, *[], **{})

    def is_callable(self):
        resp = self.get_response('get')
        self.assertEqual(resp.status_code, 200)

class QuizViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    view_class = views.QuizListView

    def test_get(self):
        self.is_callable()


class ViewTestMixin(object):
    """Mixin with shortcuts for view tests."""
    longMessage = True # More verbose error messages
    view_class = None

    def get_view_kwargs(self):
        """
        Returns a dictionary representing the view's kwargs, if necessary.

        If the URL of this view is constructed via kwargs, you can override this method and return the proper kwargs for the test.
        """
        return {}
    
    def get_response(self, method, user, data, args, kwargs):
        factory = RequestFactory()
        req_kwargs = {}
        if data:
            req_kwargs.updata({'data': data})
        req = getattr(factory, method)('/', **req_kwargs)
        req.user = user if user else User()
        return self.view_class.as_view()(req, *args, **kwargs)

    def is_callable(
        self,
        user = None,
        post = False,
        to = None,
        data = {},
        args = [],
        kwargs = {},
    ):
        """Initiates a call and tests the outcome."""
        view_kwargs = kwargs or self.get_view_kwargs()
        resp = self.get_response(
            'post' if post else 'get',
            user = user,
            data = data,
            args = args,
            kwargs = view_kwargs,
        )
        if to:
            self.assertIn(resp.status_code, [301, 302],
                            msg='The request was not redirected.')
            name = resp.url.split('?')[0].split('#')[0].url_name
            try:
                self.assertEqual(
                    resolve(name, to, msg='Should redirect to "{}".'.format(to))
                )
            except Resolver404:
                raise Exception(
                    'Could not resolve "{}".'.format(resp.url)
                )
        else:
            self.assertEqual(resp.status_code, 200)
    
    def is_not_callable(self, **kwargs):
        """Tests if call raises a 404."""
        with self.assertRaises(Http404):
            self.is_callable(**kwargs)