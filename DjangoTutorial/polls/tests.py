import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ Return False if question was publish in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ Return False if question is older than 1 day """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ Return True if question was published within the last day """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def genDate(days):
    return timezone.now() + datetime.timedelta(days=days)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ Appropriate message displayed when no questions """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ Past questions are displayed """
        Question.objects.create(question_text="Past Question.",
                                pub_date=genDate(-30))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question.>'])

    def test_future_question(self):
        """ Future questions are not displayed """
        Question.objects.create(question_text="Future Question.",
                                pub_date=genDate(30))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """ Only display past questions if both exist """
        Question.objects.create(question_text="Past Question.",
                                pub_date=genDate(-30))
        Question.objects.create(question_text="Furture Question.",
                                pub_date=genDate(30))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question.>'])

    def test_two_past_question(self):
        """ Displays multiple past questions """
        Question.objects.create(question_text='Past Question 1.',
                                pub_date=genDate(-30))
        Question.objects.create(question_text='Past Question 2.',
                                pub_date=genDate(-10))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question 2.>', '<Question: Past Question 1.>'])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """ Questions future pub will return 404 """
        future_question = Question.objects.create(question_text='Future Question.',
                                                  pub_date=genDate(30))
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ Questions past pub will display text """
        past_question = Question.objects.create(question_text="Past Question.",
                                                pub_date=genDate(-5))
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
