from books.models import History
from django import template

register = template.Library()


@register.simple_tag
def favourite_quantity(request):
    return request.user.favourite_books.all().count()

@register.simple_tag
def history_quantity(request):
    return History.objects.filter(user=request.user).count()
