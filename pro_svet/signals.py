from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import UserProfile, LevelThreshold


@receiver(pre_save, sender=UserProfile)
def update_user_level_on_xp_change(sender, instance, **kwargs):
    """
    Сигнал, который вызывается перед сохранением UserProfile
    Обновляет уровень пользователя, если XP изменилось
    """
    if instance.pk:  # Только для существующих объектов
        try:
            # Получаем старый объект из базы
            old_instance = UserProfile.objects.get(pk=instance.pk)
            
            # Проверяем, изменилось ли XP
            if old_instance.xp != instance.xp:
                # Найти максимальный порог, который достигнут
                thresholds = LevelThreshold.objects.order_by('-xp_required')
                for threshold in thresholds:
                    if instance.xp >= threshold.xp_required:
                        instance.level = threshold.level_number
                        break
                else:
                    instance.level = 0  # Если XP ниже всех порогов, уровень 0
        except UserProfile.DoesNotExist:
            # Объект новый, уровень будет рассчитан при первом сохранении
            pass