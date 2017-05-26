import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question



class QuestionMethodTests(TestCase):
#1
	def test_was_published_recently_with_future_question(self):
	#should return false for questions whose pub-date is in the future
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
	#should return False for questions whose pub-date is older than 1 day
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
	#should return True for questions whose pub-date is within the last day
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	#creates a quest with given quest_text and published the given days offset to now
	#will be negative questions published in past and positive for questions yet to be published

	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
	#if no quest exists, a msg will display
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
	# quest with pubdate in past should be displayed on index page
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_with_a_future_question(self):
	#quest with pubdate in future should not be displayed on index page
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self. assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_with_future_question_and_past_question(self):
	#if both past and future quest exist, only past should be displayed
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_view_with_two_past_questions(self):
	#quest index page may display multiple questions
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
	#the detail view of a quest with pubdate sin the future should return 404
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
	#the detail view of a quest with pubdate in past should display quest text
		past_question = create_question(question_text='Past Question.', days=-5)
		url = reverse('polls:detail',args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)
# Create your tests here.
#####
