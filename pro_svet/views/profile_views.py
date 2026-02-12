"""
Profile views for the Prosvet application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from pro_svet.models import UserProfile, UserDependency, LevelThreshold, DailyRecord


@login_required
def relapse_button_view(request, user_dependency_id):
    """
    Обработка нажатия кнопки "Сорвался"
    """
    user_dependency = UserDependency.objects.get(id=user_dependency_id, user=request.user)
    
    # Получаем профиль пользователя
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Проверяем, существует ли уже запись на сегодня
    today = timezone.now().date()
    
    # Получаем или создаем запись за сегодня
    today_record, created = DailyRecord.objects.get_or_create(
        user_dependency=user_dependency,
        date=today,
        defaults={'is_abstinent': True}  # По умолчанию считаем, что пользователь воздерживается
    )
    
    # Проверяем, есть ли в заметке информация о предыдущих срывах сегодня
    note_data = today_record.note.split('|') if today_record.note else []
    relapse_attempts = [item for item in note_data if item.startswith('relapse:')]
    
    if relapse_attempts:
        # Пользователь уже нажимал кнопку "Сорвался" сегодня
        messages.info(request, f'Вы уже фиксировали срыв сегодня для "{user_dependency.dependency.name}". Повторное нажатие невозможно.')
        return redirect('profile')
    else:
        # Это первый и единственный срыв сегодня - отнимаем 5 XP
        user_profile.xp -= 5
        user_profile.xp = max(0, user_profile.xp)  # Не допускаем отрицательный XP
        
        # Помечаем, что была попытка срыва (добавляем в заметку)
        note_data.append('relapse:1')
        today_record.note = '|'.join(note_data)
        today_record.is_abstinent = False  # Помечаем, что был срыв
        today_record.save()
        
        # Увеличиваем счетчик срывов
        user_dependency.relapse_count += 1
        
        user_profile.save()  # Level will be updated via signal
        user_dependency.save()
        
        messages.warning(request, f'Срыв зафиксирован для "{user_dependency.dependency.name}". Отнято 5 XP. Серия пока не прервана.')
    
    return redirect('profile')


@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_dependencies = request.user.userdependency_set.all()

    # Calculate next level progress
    from pro_svet.models import LevelThreshold
    current_level_threshold = LevelThreshold.objects.filter(xp_required__lte=user_profile.xp).order_by('-xp_required').first()
    next_level_threshold = LevelThreshold.objects.filter(xp_required__gt=user_profile.xp).order_by('xp_required').first()
    
    progress_data = {}
    if current_level_threshold and next_level_threshold:
        progress_data['current_level'] = current_level_threshold.level_number
        progress_data['next_level'] = next_level_threshold.level_number
        progress_data['current_xp'] = user_profile.xp
        progress_data['xp_for_current'] = current_level_threshold.xp_required
        progress_data['xp_for_next'] = next_level_threshold.xp_required
        progress_data['progress_percent'] = min(100, round(((user_profile.xp - current_level_threshold.xp_required) / 
                                   (next_level_threshold.xp_required - current_level_threshold.xp_required)) * 100))
    elif current_level_threshold:
        # User has reached the highest level
        progress_data['current_level'] = current_level_threshold.level_number
        progress_data['next_level'] = current_level_threshold.level_number
        progress_data['current_xp'] = user_profile.xp
        progress_data['xp_for_current'] = current_level_threshold.xp_required
        progress_data['xp_for_next'] = current_level_threshold.xp_required
        progress_data['progress_percent'] = 100
    else:
        # User is at level 0
        next_level_threshold = LevelThreshold.objects.order_by('xp_required').first()
        if next_level_threshold:
            progress_data['current_level'] = 0
            progress_data['next_level'] = next_level_threshold.level_number
            progress_data['current_xp'] = user_profile.xp
            progress_data['xp_for_current'] = 0
            progress_data['xp_for_next'] = next_level_threshold.xp_required
            progress_data['progress_percent'] = min(100, round((user_profile.xp / next_level_threshold.xp_required) * 100))
        else:
            # No level thresholds defined
            progress_data['current_level'] = 0
            progress_data['next_level'] = 0
            progress_data['current_xp'] = user_profile.xp
            progress_data['xp_for_current'] = 0
            progress_data['xp_for_next'] = 0
            progress_data['progress_percent'] = 0

    if request.method == 'POST':
        # Handle daily abstinence marking
        dependency_id = request.POST.get('dependency_id')
        if dependency_id:
            user_dependency = UserDependency.objects.get(id=dependency_id, user=request.user)

            # Check if record already exists for today
            today = timezone.now().date()
            today_record, created = DailyRecord.objects.get_or_create(
                user_dependency=user_dependency,
                date=today,
                defaults={'is_abstinent': True}
            )

            # Check if there's already a relapse recorded for today
            note_data = today_record.note.split('|') if today_record.note else []
            relapse_attempts = [item for item in note_data if item.startswith('relapse:')]
            
            if relapse_attempts:
                # A relapse has already been recorded today, so abstinence marking is not allowed
                messages.warning(request, f'Невозможно отметить день воздержания для "{user_dependency.dependency.name}", так как сегодня уже был зафиксирован срыв.')
            elif not created and today_record.is_abstinent:
                # Record already exists and is marked as abstinent today
                messages.warning(request, f'Сегодняшний день уже был отмечен для "{user_dependency.dependency.name}"')
            else:
                # Either new record or existing record that wasn't marked as abstinent
                if not today_record.is_abstinent:
                    # Update record to mark as abstinent
                    today_record.is_abstinent = True
                    today_record.save()

                # Award XP for daily abstinence (award if it's a new record or if it wasn't previously marked)
                user_profile.xp += 10  # 10 XP per day of abstinence
                user_profile.save()  # Level will be updated via signal

                # Update user dependency stats
                # Only increment streak if this is consecutive day or first day
                from datetime import timedelta
                if (not user_dependency.last_day_of_abstinence or
                    user_dependency.last_day_of_abstinence == today - timedelta(days=1)):
                    user_dependency.current_streak += 1
                else:
                    # If there was a break, reset streak to 1 (or keep as 1 if it was 0)
                    user_dependency.current_streak = 1

                user_dependency.total_days_abstained += 1
                user_dependency.last_day_of_abstinence = today
                user_dependency.save()

                messages.success(request, f'Отметка о воздержании проставлена для "{user_dependency.dependency.name}". Начислено 10 XP!')

    context = {
        'user_profile': user_profile,
        'user_dependencies': user_dependencies,
        'progress_data': progress_data,
    }
    return render(request, 'profile.html', context=context)