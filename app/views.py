from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from app import models
from django.contrib import auth
from app.forms import LoginForm, SignupForm, AnswerForm, AskQuestion
from app.models import Tag, Question, Answer, Profile


# Create your views here.

def paginate(object_list, request, per_page=5):
    paginator = Paginator(object_list, per_page)
    page = request.GET.get('page', 1)
    try:
        paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        raise Http404("Page not found")
    return paginator.page(page)

def index(request):
    questions = paginate(models.Question.objects.get_new_questions(), request)
    context = {
        'questions': questions,
        'page_obj': questions,
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }

    return render(request, 'index.html', context=context)


def hot(request):
    questions = paginate(models.Question.objects.get_hot_questions(), request)
    context = {
        'questions': questions,
        'page_obj': questions,
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'hot.html', context=context)


def question(request, question_id):
    answers = paginate(models.Answer.objects.get_answers(question_id), request)
    question = get_object_or_404(models.Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            question.amount_of_answers += 1
            question.save(update_fields=['amount_of_answers'])
            return redirect('question', question_id=question.id)
    else:
        form = AnswerForm()
    context = {
        'question': question,
        'answers': answers,
        'tags': models.Tag.objects.get_popular_tags(),
        'page_obj': answers,
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'question.html', context=context)


def tag(request, tag_name):
    questions = paginate(models.Question.objects.get_questions_by_tag(tag_name), request)
    context = {
        'tag_name': tag_name,
        'questions': questions,
        'page_obj': questions,
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'tag.html', context=context)

@login_required(login_url=reverse_lazy('login'))
def ask(request):
    if request.method == 'POST':
        form = AskQuestion(request.POST, request.user)
        if form.is_valid():
            question = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            question.author = profile
            question.save()
            raw = form.cleaned_data['tags']
            names = {name for name in raw if name}
            for name in names:
                tag_obj, created = Tag.objects.get_or_create(name=name)
                question.tags.add(tag_obj)
            return redirect('question', question_id=question.id)
    else:
        form = AskQuestion()

    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'ask.html', context=context)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print(username, password)
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                form.add_error(field=None, error='User not found!')
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(reverse('index'))
    else:
        form = SignupForm()
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'signup.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))



def settings(request):
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'settings.html', context=context)