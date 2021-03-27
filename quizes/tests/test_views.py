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