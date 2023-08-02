from django import template

register = template.Library()

@register.filter
def seconds_to_mins_secs(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins}분 {secs}초"