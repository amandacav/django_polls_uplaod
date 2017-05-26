#from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
#from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

#Index 1
#def index(request):
	#return HttpResponse("Hello, world. You're at the polls index.")

#Index 2
#def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)

#Index 3
"""def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {'latest_question_list' : latest_question_list,}
	return HttpResponse(template.render(context, request))"""

#Index 4
"""def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)"""

#Index 5
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	#QS 1
#	def get_queryset(self):
	#Return the last five published questions
#		return Question.objects.order_by('-pub_date')[:5]
	#QS 2
	def get_queryset(self):
	#Return the last five published questions (not including those published in the future)	
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

#3 below are possible conversions from Py2 to Py3?
#def detail(request, question_id):
	#return HttpResponse("You're looking at question{s!}.".format(question_id))

#def results(request, question_id):
	#return HttpResponse("You're looking at the results of question{s!}.".format(question_id))

#def vote(reqeust, question_id):
	#return HttpResponse("You're voting on question{s!}.".format(question_id))

#Detail 1
"""def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)"""

#Detail 2
"""def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})"""

#Detail 3
"""def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question' : question})"""

#Detail 4
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
	#excludes quest that aren't published yet
		return Question.objects.filter(pub_date__lte=timezone.now())

#results 1
"""def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)"""

#Results 2
"""def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})"""

#Results 3
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

#Vote 1
"""def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)"""

#Vote 2
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form.
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.", })
	else :
		selected_choice.votes += 1
		selected_choice.save()
	#Always return an Http ResponseRedirect after successfully dealing with POST data.
	#This prevents data from being posted twice if a user hits the Back button
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
