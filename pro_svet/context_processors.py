from .models import UserProfile


def user_profile_processor(request):
    """
    Adds the user profile to the context for all requests
    """
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return {'user_profile': profile}
    return {'user_profile': None}