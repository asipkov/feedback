from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Rating
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdmin(UserAdmin):
    inlines = (UserInline,)


admin.site.register(Comment, CommentAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
