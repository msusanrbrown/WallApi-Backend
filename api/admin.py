from django.contrib import admin
from .models import STATUS, User, Post, Like


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email', 'username', 'first_name', 'last_name']
#     list_display = ('email', 'username', 'first_name', 'last_name', 'number_of_posts')
#     list_filter = ['date_joined', 'is_active', 'is_staff']
#     # raw_id_fields = ['user', 'cohort']
#     actions = []

#     def number_of_posts(self, obj):
#         return Post.objects.filter(user__id=obj.id).count()

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name']
    list_display = ('user','likes', 'dislikes', 'is_deleted')
    list_filter = ['is_deleted']
    # raw_id_fields = ['user', 'cohort']
    actions = []

    def likes(self, obj):
        return Like.objects.filter(post=obj, status='LIKE').count()

    def dislikes(self, obj):
        return Like.objects.filter(post=obj, status='DISLIKE').count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name']
    list_display = ('user','status')
    list_filter = ['status']
    # raw_id_fields = ['user', 'cohort']
    actions = []

    