from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.cache import cache
from app.models import Question, Answer, Tag, Profile
from app.models import QuestionLike, AnswerLike
from datetime import timedelta
from django.db.models import Count, Q


class Command(BaseCommand):
    help = "Кэширует популярные теги и лучших пользователей"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        recent_questions = Question.objects.filter(
            created_at__gte=now - timedelta(days=90)
        )

        popular_tags = Tag.objects.filter(
            question__in=recent_questions
        ).annotate(
            question_count=Count("question")
        ).order_by("-question_count")[:10]

        cache.set("popular_tags", list(popular_tags), timeout=3600)
        week_ago = now - timedelta(days=7)

        top_questions = Question.objects.filter(
            created_at__gte=week_ago
        ).annotate(
            like_count=Count("questionlike", filter=Q(questionlike__like=True))
        ).order_by("-like_count")

        top_answers = Answer.objects.filter(
            created_at__gte=week_ago
        ).annotate(
            like_count=Count("answerlike", filter=Q(answerlike__like=True))
        ).order_by("-like_count")
        profile_scores = {}

        for q in top_questions:
            profile_scores[q.author_id] = profile_scores.get(q.author_id, 0) + q.like_count

        for a in top_answers:
            profile_scores[a.author_id] = profile_scores.get(a.author_id, 0) + a.like_count

        sorted_profiles = sorted(
            profile_scores.items(), key=lambda x: x[1], reverse=True
        )[:10]

        top_user_ids = [uid for uid, _ in sorted_profiles]
        top_users = Profile.objects.filter(id__in=top_user_ids)

        cache.set("best_users", list(top_users), timeout=3600)

        self.stdout.write(self.style.SUCCESS("✔ Кэш обновлён: popular_tags + best_users"))
