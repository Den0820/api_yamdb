from django.contrib import admin

from reviews.models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass