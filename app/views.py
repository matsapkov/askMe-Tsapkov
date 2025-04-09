from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from app import models

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
    context = {
        'question': question,
        'answers': answers,
        'tags': models.Tag.objects.get_popular_tags(),
        'page_obj': answers,
        'profiles': models.Profile.objects.get_popular_profiles(),
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

def ask(request):
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'ask.html', context=context)


def login(request):
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'login.html', context=context)


def signup(request):
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'signup.html', context=context)


def settings(request):
    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'settings.html', context=context)