from django import template
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag("includes/popular_tags.html")
def popular_tags():
    return {"tags": cache.get("popular_tags", [])}


@register.inclusion_tag("includes/best_users.html")
def best_users():
    return {"profiles": cache.get("best_users", [])}
