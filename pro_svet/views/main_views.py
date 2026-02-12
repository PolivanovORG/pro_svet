"""
Main views for the Prosvet application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from pro_svet.models import UserProfile, Dependency, UserDependency, LevelThreshold, DependencyLevel, DailyRecord


def get_user_profile_context(user):
    """Helper function to get user profile, creating it if it doesn't exist"""
    if user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        return {'user_profile': user_profile}
    return {'user_profile': None}


def home_view(request):
    """Main page showing all dependencies"""
    dependencies = Dependency.objects.filter(is_preset=True)  # Show only preset dependencies

    context = {
        'dependencies': dependencies
    }
    return render(request, 'home.html', context=context)


def dependency_detail_view(request, slug):
    """Detail page for a specific dependency"""
    dependency = Dependency.objects.get(slug=slug)

    # Check if user has this dependency registered
    user_dependency = None
    if request.user.is_authenticated:
        user_dependency, created = UserDependency.objects.get_or_create(
            user=request.user,
            dependency=dependency
        )

    context = {
        'dependency': dependency,
        'user_dependency': user_dependency
    }
    return render(request, 'dependency_detail.html', context=context)


@login_required
def mark_dependency_not_having(request, slug):
    """Mark that the user doesn't have this dependency"""
    dependency = Dependency.objects.get(slug=slug)
    user_dependency, created = UserDependency.objects.get_or_create(
        user=request.user,
        dependency=dependency
    )

    # Check if the user has already started treatment (has a level set)
    if user_dependency.level:
        # User has already started treatment, prevent from marking as not having
        messages.error(request, f'Невозможно отметить, что у вас нет зависимости "{dependency.name}", так как вы уже начали лечение.')
    elif not user_dependency.is_active:
        # User has already marked this, don't award XP again
        messages.info(request, f'Вы уже отметили, что у вас нет зависимости "{dependency.name}"')
    else:
        # Mark as not having and award XP
        user_dependency.is_active = False
        user_dependency.save()

        # Award experience for marking dependency as not having
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.xp += 100  # Award 100 XP as specified in requirements
        user_profile.save()  # Level will be updated via signal

        messages.success(request, f'Вы отметили, что у вас нет зависимости "{dependency.name}". Начислено 100 XP!')

    return redirect('dependency_detail', slug=slug)


@login_required
def assess_dependency_level(request, slug):
    """Start the assessment process for dependency level"""
    dependency = Dependency.objects.get(slug=slug)

    # Check if user has already marked this dependency as not having
    user_dependency, created = UserDependency.objects.get_or_create(
        user=request.user,
        dependency=dependency
    )

    # If user previously marked that they don't have this dependency, penalize them
    if user_dependency.is_active == False:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.xp = max(0, user_profile.xp - 100)  # Subtract 100 XP, but don't go below 0
        user_profile.save()  # Level will be updated via signal

        messages.warning(request, f'Вы снова решили определить уровень зависимости "{dependency.name}". За это решение с вас снято 100 XP.')

    # Get available levels for this dependency
    levels = DependencyLevel.objects.filter(dependency=dependency)

    context = {
        'dependency': dependency,
        'levels': levels
    }
    return render(request, 'dependency_assessment.html', context=context)


@login_required
def submit_assessment(request, slug):
    """Submit the assessment and determine dependency level"""
    if request.method != 'POST':
        return redirect('home')

    dependency = Dependency.objects.get(slug=slug)

    # Check if user has already set a level for this dependency
    user_dependency, created = UserDependency.objects.get_or_create(
        user=request.user,
        dependency=dependency
    )

    if user_dependency.level:
        # User has already set a level, prevent from changing it
        messages.error(request, f'Невозможно изменить уровень зависимости "{dependency.name}", так как вы уже определили уровень.')
        return redirect('dependency_detail', slug=slug)

    # Get selected level from form
    level_id = request.POST.get('level')
    if level_id:
        level = DependencyLevel.objects.get(id=level_id, dependency=dependency)

        # Update user dependency with the selected level
        user_dependency.level = level
        user_dependency.is_active = True  # Mark as active since user is assessing it
        user_dependency.start_date = timezone.now().date()
        user_dependency.save()

        messages.success(request, f'Уровень зависимости "{dependency.name}" определен как {level.get_level_display()}. Лечение начато.')

    return redirect('dependency_detail', slug=slug)