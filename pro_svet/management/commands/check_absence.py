from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from pro_svet.models import UserProfile, UserDependency, DailyRecord


class Command(BaseCommand):
    help = 'Проверяет и обрабатывает долгое отсутствие пользователей'

    def handle(self, *args, **options):
        self.stdout.write('Запуск проверки долгого отсутствия...')
        
        # Получаем всех пользователей с активными зависимостями
        user_profiles = UserProfile.objects.filter(
            user__userdependency__is_active=True
        ).distinct()
        
        processed_users = 0
        
        for user_profile in user_profiles:
            self.process_user_absence(user_profile)
            processed_users += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Проверка завершена. Обработано пользователей: {processed_users}')
        )

    def process_user_absence(self, user_profile):
        """Обрабатывает долгое отсутствие для одного пользователя"""
        user_dependencies = UserDependency.objects.filter(
            user=user_profile.user,
            is_active=True
        )
        
        for user_dependency in user_dependencies:
            # Проверяем, есть ли записи за последние 48 часов
            two_days_ago = timezone.now().date() - timedelta(days=2)
            
            # Получаем последнюю запись для этой зависимости
            last_record = DailyRecord.objects.filter(
                user_dependency=user_dependency
            ).order_by('-date').first()
            
            if last_record and last_record.date < two_days_ago:
                # Прошло более 48 часов с последней активности
                if user_profile.auto_continue_streak:
                    # Автопродление серии: создаем записи за пропущенные дни как воздержание
                    self.handle_auto_continuation(user_profile, user_dependency, last_record)
                else:
                    # Фиксируем срыв: создаем запись о срыве за последний день
                    self.handle_absence_penalty(user_profile, user_dependency, last_record)

    def handle_auto_continuation(self, user_profile, user_dependency, last_record):
        """Обработка автопродления серии"""
        current_date = last_record.date + timedelta(days=1)
        today = timezone.now().date()
        
        while current_date <= today:
            # Создаем запись о воздержании за пропущенный день
            DailyRecord.objects.get_or_create(
                user_dependency=user_dependency,
                date=current_date,
                defaults={'is_abstinent': True}
            )
            
            # Обновляем статистику зависимости
            user_dependency.current_streak += 1
            user_dependency.total_days_abstained += 1
            user_dependency.last_day_of_abstinence = current_date
            user_dependency.save()
            
            # Начисляем 10 XP за каждый день
            user_profile.xp += 10
            user_profile.save()  # Уровень обновится через сигнал
            
            current_date += timedelta(days=1)

    def handle_absence_penalty(self, user_profile, user_dependency, last_record):
        """Обработка штрафа за долгое отсутствие"""
        today = timezone.now().date()
        
        # Помечаем сегодняшний день как срыв
        today_record, created = DailyRecord.objects.get_or_create(
            user_dependency=user_dependency,
            date=today,
            defaults={'is_abstinent': False}
        )
        
        if not created:
            today_record.is_abstinent = False
            today_record.save()
        
        # Добавляем информацию о срыве в заметку
        note_data = today_record.note.split('|') if today_record.note else []
        if 'absence_penalty' not in note_data:
            note_data.append('absence_penalty')
            today_record.note = '|'.join(note_data)
            today_record.save()
        
        # Уменьшаем серию (но не меньше 0)
        user_dependency.current_streak = max(0, user_dependency.current_streak - 1)
        
        # Уменьшаем XP на 10 за каждый пропущенный день
        days_missed = min((today - last_record.date).days, 30)  # Ограничиваем штраф 30 днями
        xp_penalty = min(user_profile.xp, days_missed * 10)  # Не уходим в минус
        user_profile.xp -= xp_penalty
        
        user_dependency.save()
        user_profile.save()  # Уровень обновится через сигнал