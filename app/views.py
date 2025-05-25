from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from app import models
from django.contrib import auth
from app.forms import LoginForm, SignupForm, AnswerForm, AskQuestion, SettingsForm
from app.models import Tag, Question, Answer, Profile, QuestionLike, AnswerLike


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
    qs = models.Question.objects.get_new_questions()
    page = paginate(qs, request)
    questions_data = []
    for q in page:
        cnt = QuestionLike.objects.filter(question=q, like=True).count()
        me = False
        if request.user.is_authenticated:
            profile = request.user.profile
            me = QuestionLike.objects.filter(
                question=q,
                author=profile,
                like=True
            ).exists()

        questions_data.append({
            'obj': q,
            'likes_count': cnt,
            'is_liked': me,
        })

    context = {
        'questions':       questions_data,
        'page_obj':        page,
        'tags':            Tag.objects.get_popular_tags(),
        'profiles':        Profile.objects.get_popular_profiles(),
    }
    return render(request, 'index.html', context)


def hot(request):
    page = paginate(models.Question.objects.get_hot_questions(), request)

    questions_data = []
    for q in page:
        cnt = models.QuestionLike.objects.filter(question=q, like=True).count()

        liked = False
        if request.user.is_authenticated:
            liked = models.QuestionLike.objects.filter(
                question=q,
                author=request.user.profile,
                like=True
            ).exists()

        questions_data.append({
            'obj': q,
            'likes_count': cnt,
            'is_liked': liked,
        })

    context = {
        'questions': questions_data,
        'page_obj': page,
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
    }
    return render(request, 'hot.html', context=context)


def question(request, question_id):
    answers = paginate(models.Answer.objects.get_answers(question_id), request)
    q = get_object_or_404(models.Question, id=question_id)

    likes_count = models.QuestionLike.objects.filter(question=q, like=True).count()
    is_liked = False
    if request.user.is_authenticated:
        is_liked = models.QuestionLike.objects.filter(
            question=q,
            author=request.user.profile,
            like=True
        ).exists()

    answer_items = []
    for a in answers:
        liked = False
        if request.user.is_authenticated:
            liked = models.AnswerLike.objects.filter(answer=a, author=request.user.profile, like=True).exists()

        answer_items.append({
            'obj': a,
            'likes_count': models.AnswerLike.objects.filter(answer=a, like=True).count(),
            'is_liked': liked
        })

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = q
            answer.author = request.user.profile
            answer.save()
            q.amount_of_answers += 1
            q.save(update_fields=['amount_of_answers'])
            return redirect('question', question_id=q.id)
    else:
        form = AnswerForm()

    context = {
        'question': q,
        'question_item': {
            'obj': q,
            'likes_count': likes_count,
            'is_liked': is_liked,
        },
        'answers': answer_items,
        'tags': models.Tag.objects.get_popular_tags(),
        'page_obj': answers,
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'question.html', context=context)


def tag(request, tag_name):
    page = paginate(models.Question.objects.get_questions_by_tag(tag_name), request)

    questions_data = []
    for q in page:
        cnt = models.QuestionLike.objects.filter(question=q, like=True).count()

        liked = False
        if request.user.is_authenticated:
            liked = models.QuestionLike.objects.filter(
                question=q,
                author=request.user.profile,
                like=True
            ).exists()

        questions_data.append({
            'obj': q,
            'likes_count': cnt,
            'is_liked': liked,
        })

    context = {
        'tag_name': tag_name,
        'questions': questions_data,
        'page_obj': page,
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
        form = SignupForm(request.POST, request.FILES)
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
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))
    else:
        form = SettingsForm(instance=profile)

    context = {
        'tags': models.Tag.objects.get_popular_tags(),
        'profiles': models.Profile.objects.get_popular_profiles(),
        'form': form,
    }
    return render(request, 'settings.html', context=context)

@require_POST
@login_required(login_url=reverse_lazy('login'))
def like_async(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    profile = request.user.profile

    ql, created = QuestionLike.objects.get_or_create(
        question=question,
        author=profile,
        defaults={'like': True}
    )
    if not created:
        ql.like = not ql.like
        ql.save()

    # простейший подсчёт лайков
    likes_count = QuestionLike.objects.filter(
        question=question,
        like=True
    ).count()

    return JsonResponse({
        'liked': ql.like,
        'likes_count': likes_count,
    })


@require_POST
@login_required(login_url=reverse_lazy('login'))
def answer_like_async(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    profile = request.user.profile

    like_obj, created = AnswerLike.objects.get_or_create(
        answer=answer,
        author=profile,
        defaults={'like': True}
    )

    if not created:
        like_obj.like = not like_obj.like
        like_obj.save(update_fields=['like'])

    likes_count = AnswerLike.objects.filter(answer=answer, like=True).count()

    return JsonResponse({
        'liked': like_obj.like,
        'likes_count': likes_count,
    })

