from django.contrib import admin

from reviews.models import Category, Title, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass
