from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pro_svet.models import (
    Dependency, 
    DependencyLevel, 
    UserProfile, 
    Quote, 
    LevelThreshold
)


class Command(BaseCommand):
    help = 'Заполняет базу данных начальными значениями'

    def handle(self, *args, **options):
        self.stdout.write('Заполняем базу данных начальными значениями...')

        # Создаем предустановленные зависимости
        dependencies_data = [
            {
                'name': 'Игровая зависимость',
                'slug': 'gaming-addiction',
                'description': 'Чрезмерное увлечение видеоиграми, которое начинает мешать повседневной жизни, работе и социальным отношениям.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Шопоголизм',
                'slug': 'shopping-addiction',
                'description': 'Неконтролируемая потребность в покупках, часто приводящая к финансовым проблемам и стрессу.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Думскролинг (ТикТок и шортсы)',
                'slug': 'doom-scrolling',
                'description': 'Бесконечное прокручивание ленты соцсетей и просмотр коротких видео, отнимающее время и снижающее продуктивность.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Зависимость от телевидения/стриминга',
                'slug': 'tv-streaming-addiction',
                'description': 'Чрезмерное потребление телевизионного контента и сериалов, мешающее другим аспектам жизни.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Пищевая зависимость',
                'slug': 'food-addiction',
                'description': 'Неконтролируемое потребление пищи, особенно продуктов с высоким содержанием сахара, жира и соли.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Алкоголь, Наркотики и Никотин (Химическая зависимость)',
                'slug': 'chemical-dependence',
                'description': 'Физическая и психологическая зависимость от химических веществ, вызывающих изменения в работе мозга.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Лудомания',
                'slug': 'gambling-addiction',
                'description': 'Навязчивое стремление к азартным играм, несмотря на негативные последствия для финансов и отношений.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            },
            {
                'name': 'Порнография',
                'slug': 'pornography-addiction',
                'description': 'Неконтролируемое потребление порнографического контента, влияющее на сексуальное здоровье и отношения.',
                'levels': [
                    {'level': 'light', 'days_required': 150},
                    {'level': 'medium', 'days_required': 350},
                    {'level': 'heavy', 'days_required': 700}
                ]
            }
        ]

        # Создаем зависимости и уровни
        for dep_data in dependencies_data:
            dependency, created = Dependency.objects.get_or_create(
                name=dep_data['name'],
                slug=dep_data['slug'],
                defaults={
                    'description': dep_data['description'],
                    'is_preset': True
                }
            )
            
            if created:
                self.stdout.write(f'Создана зависимость: {dependency.name}')
                
                # Создаем уровни для зависимости
                for level_data in dep_data['levels']:
                    level, level_created = DependencyLevel.objects.get_or_create(
                        dependency=dependency,
                        level=level_data['level'],
                        defaults={'days_required': level_data['days_required']}
                    )
                    
                    if level_created:
                        self.stdout.write(f'  - Уровень {level.get_level_display()}: {level.days_required} дней')
        
        # Создаем пороги уровней
        level_thresholds = [
            {'level_number': 1, 'xp_required': 0},
            {'level_number': 2, 'xp_required': 500},
            {'level_number': 3, 'xp_required': 1500},
            {'level_number': 4, 'xp_required': 3000},
            {'level_number': 5, 'xp_required': 5000},
            {'level_number': 6, 'xp_required': 7500},
            {'level_number': 7, 'xp_required': 10000},
            {'level_number': 8, 'xp_required': 15000},
            {'level_number': 9, 'xp_required': 20000},
            {'level_number': 10, 'xp_required': 30000},
        ]
        
        for threshold_data in level_thresholds:
            threshold, created = LevelThreshold.objects.get_or_create(
                level_number=threshold_data['level_number'],
                defaults={'xp_required': threshold_data['xp_required']}
            )
            
            if created:
                self.stdout.write(f'Порог уровня {threshold.level_number}: {threshold.xp_required} XP')

        # Создаем мотивационные цитаты
        quotes_data = [
            {
                'text': 'Путь тысячи миль начинается с одного шага.',
                'author': 'Лао Цзы'
            },
            {
                'text': 'Лучший способ сделать это — просто начать.',
                'author': 'Марк Твен'
            },
            {
                'text': 'Не бойся медленного прогресса, бойся стояния на месте.',
                'author': 'Конфуций'
            },
            {
                'text': 'Каждый срыв — это возможность начать заново.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Ты сильнее своих искушений.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Сегодняшние усилия — завтрашние результаты.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Изменения возможны, когда ты веришь в себя.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Ты уже преодолел больше, чем думаешь.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Каждый день без зависимости — победа.',
                'author': 'Неизвестный'
            },
            {
                'text': 'Твоя сила внутри тебя, используй её.',
                'author': 'Неизвестный'
            }
        ]
        
        for quote_data in quotes_data:
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                author=quote_data['author'],
                defaults={'is_active': True}
            )
            
            if created:
                self.stdout.write(f'Цитата: "{quote.text[:30]}..." - {quote.author}')

        # Создаем суперпользователя, если он не существует
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            # Создаем профиль для администратора
            UserProfile.objects.get_or_create(user=admin_user)
            self.stdout.write('Создан суперпользователь: admin / admin123')

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена начальными значениями!')
        )