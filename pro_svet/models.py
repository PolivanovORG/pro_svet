from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Dependency(models.Model):
    """
    Модель зависимости (предустановленные или созданные пользователем)
    """
    name = models.CharField(max_length=200, verbose_name="Название зависимости")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор")
    description = models.TextField(verbose_name="Описание зависимости")
    is_preset = models.BooleanField(default=True, verbose_name="Предустановленная зависимость")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name="Создано пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Зависимость"
        verbose_name_plural = "Зависимости"


class DependencyLevel(models.Model):
    """
    Уровень зависимости (легкий, средний, тяжелый)
    """
    LEVEL_CHOICES = [
        ('light', 'Легкий'),
        ('medium', 'Средний'),
        ('heavy', 'Тяжелый'),
    ]
    
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, verbose_name="Зависимость")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name="Уровень")
    days_required = models.PositiveIntegerField(verbose_name="Количество дней для лечения")
    
    def __str__(self):
        return f"{self.dependency.name} - {self.get_level_display()}"

    class Meta:
        verbose_name = "Уровень зависимости"
        verbose_name_plural = "Уровни зависимости"


class UserProfile(models.Model):
    """
    Профиль пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    xp = models.IntegerField(default=0, verbose_name="Очки опыта")
    level = models.IntegerField(default=0, verbose_name="Уровень просветления")
    quote_notifications_enabled = models.BooleanField(default=True, verbose_name="Уведомления с цитатами")
    
    def __str__(self):
        return f"Профиль {self.user.username}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class UserDependency(models.Model):
    """
    Зависимость конкретного пользователя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, verbose_name="Зависимость")
    level = models.ForeignKey(DependencyLevel, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="Уровень зависимости")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    is_completed = models.BooleanField(default=False, verbose_name="Завершена")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала лечения")
    last_day_of_abstinence = models.DateField(null=True, blank=True, verbose_name="Последний день воздержания")
    current_streak = models.PositiveIntegerField(default=0, verbose_name="Текущая серия дней")
    total_days_abstained = models.PositiveIntegerField(default=0, verbose_name="Всего дней воздержания")
    relapse_count = models.PositiveIntegerField(default=0, verbose_name="Количество срывов")
    
    def __str__(self):
        return f"{self.user.username} - {self.dependency.name}"

    class Meta:
        unique_together = ['user', 'dependency']
        verbose_name = "Пользовательская зависимость"
        verbose_name_plural = "Пользовательские зависимости"


class DailyRecord(models.Model):
    """
    Ежедневная запись прогресса пользователя
    """
    user_dependency = models.ForeignKey(UserDependency, on_delete=models.CASCADE, verbose_name="Зависимость пользователя")
    date = models.DateField(verbose_name="Дата")
    is_abstinent = models.BooleanField(default=False, verbose_name="Было воздержание")
    note = models.TextField(blank=True, verbose_name="Заметка")
    
    def __str__(self):
        return f"{self.user_dependency.user.username} - {self.date}: {'+' if self.is_abstinent else '-'}"

    class Meta:
        unique_together = ['user_dependency', 'date']
        verbose_name = "Ежедневная запись"
        verbose_name_plural = "Ежедневные записи"


class Quote(models.Model):
    """
    Мотивирующая цитата дня
    """
    text = models.TextField(verbose_name="Текст цитаты")
    author = models.CharField(max_length=200, verbose_name="Автор")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    def __str__(self):
        return f"Цитата от {self.author}"

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"


class Habit(models.Model):
    """
    Полезная привычка
    """
    name = models.CharField(max_length=200, verbose_name="Название привычки")
    description = models.TextField(verbose_name="Описание")
    xp_reward = models.PositiveIntegerField(default=10, verbose_name="Награда за выполнение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"


class HabitCompletion(models.Model):
    """
    Выполнение полезной привычки
    """
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name="Привычка")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateField(verbose_name="Дата выполнения")
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"

    class Meta:
        unique_together = ['habit', 'date']
        verbose_name = "Выполнение привычки"
        verbose_name_plural = "Выполнения привычек"


class LevelThreshold(models.Model):
    """
    Пороги для уровней просветления
    """
    level_number = models.PositiveIntegerField(unique=True, verbose_name="Номер уровня")
    xp_required = models.PositiveIntegerField(verbose_name="Необходимо XP")
    
    def __str__(self):
        return f"Уровень {self.level_number} ({self.xp_required} XP)"

    class Meta:
        verbose_name = "Порог уровня"
        verbose_name_plural = "Пороги уровней"


class Relapse(models.Model):
    """
    Запись о срыве пользователя
    """
    user_dependency = models.ForeignKey(UserDependency, on_delete=models.CASCADE, verbose_name="Зависимость пользователя")
    date = models.DateField(verbose_name="Дата срыва")
    reason = models.TextField(blank=True, verbose_name="Причина срыва")
    
    def __str__(self):
        return f"Срыв {self.user_dependency.user.username} - {self.user_dependency.dependency.name} ({self.date})"

    class Meta:
        verbose_name = "Срыв"
        verbose_name_plural = "Срывы"