from django import template
from django.utils import timezone
from pro_svet.models import DailyRecord

register = template.Library()


@register.simple_tag
def has_daily_record_for_today(user_dependency):
    """Check if the user has already recorded abstinence for today"""
    today = timezone.now().date()
    try:
        record = DailyRecord.objects.get(
            user_dependency=user_dependency,
            date=today
        )
        return record.is_abstinent
    except DailyRecord.DoesNotExist:
        return False


@register.simple_tag
def has_relapse_for_today(user_dependency):
    """Check if the user has recorded a relapse for today"""
    today = timezone.now().date()
    try:
        record = DailyRecord.objects.get(
            user_dependency=user_dependency,
            date=today
        )
        # Check if there's a relapse recorded in the note field
        note_data = record.note.split('|') if record.note else []
        relapse_attempts = [item for item in note_data if item.startswith('relapse:')]
        return bool(relapse_attempts)
    except DailyRecord.DoesNotExist:
        return False


@register.simple_tag
def has_any_record_for_today(user_dependency):
    """Check if the user has any record for today (abstinence or relapse)"""
    today = timezone.now().date()
    try:
        record = DailyRecord.objects.get(
            user_dependency=user_dependency,
            date=today
        )
        return True
    except DailyRecord.DoesNotExist:
        return False


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key)