from django.contrib import admin
from .models import (
    Dependency, 
    DependencyLevel, 
    UserProfile, 
    UserDependency, 
    DailyRecord, 
    Quote, 
    Habit, 
    HabitCompletion, 
    LevelThreshold, 
    Relapse
)


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_preset', 'created_at')
    list_filter = ('is_preset',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Regular admins can only see preset dependencies
        return qs.filter(is_preset=True)


@admin.register(DependencyLevel)
class DependencyLevelAdmin(admin.ModelAdmin):
    list_display = ('dependency', 'level', 'days_required')
    list_filter = ('level', 'dependency')
    search_fields = ('dependency__name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp', 'level', 'quote_notifications_enabled')
    list_filter = ('quote_notifications_enabled',)
    search_fields = ('user__username', 'user__email')


@admin.register(UserDependency)
class UserDependencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'dependency', 'level', 'is_active', 'current_streak', 'start_date')
    list_filter = ('is_active', 'is_completed', 'level', 'dependency')
    search_fields = ('user__username', 'dependency__name')
    date_hierarchy = 'start_date'


@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ('user_dependency', 'date', 'is_abstinent')
    list_filter = ('is_abstinent', 'date')
    search_fields = ('user_dependency__user__username', 'user_dependency__dependency__name')
    date_hierarchy = 'date'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'text_truncated', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text', 'author')

    def text_truncated(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_truncated.short_description = 'Текст цитаты'


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'xp_reward')
    list_filter = ('user',)
    search_fields = ('name', 'description', 'user__username')


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'user', 'date')
    list_filter = ('date', 'user')
    search_fields = ('habit__name', 'user__username')
    date_hierarchy = 'date'


@admin.register(LevelThreshold)
class LevelThresholdAdmin(admin.ModelAdmin):
    list_display = ('level_number', 'xp_required')
    ordering = ('level_number',)


@admin.register(Relapse)
class RelapseAdmin(admin.ModelAdmin):
    list_display = ('user_dependency', 'date', 'relapse_info')
    list_filter = ('date', 'user_dependency__user', 'user_dependency__dependency')
    search_fields = ('user_dependency__user__username', 'user_dependency__dependency__name')
    date_hierarchy = 'date'

    def relapse_info(self, obj):
        return f"{obj.user_dependency.user.username} - {obj.user_dependency.dependency.name}"
    relapse_info.short_description = 'Информация о срыве'