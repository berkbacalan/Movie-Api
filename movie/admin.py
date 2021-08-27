from django.contrib import admin

from movie.models import Movie, Category, Subcategory


class MovieAdmin(admin.ModelAdmin):
    model = Movie

    list_display = ['name', 'publish_date', 'director']
    list_filter = ['name', 'publish_date', 'category', 'director']
    search_fields = ['name']


admin.site.register(Movie, MovieAdmin)


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    model = Subcategory

    list_filter = ['name', 'parent_category']
    list_display = ['name', 'parent_category']
    search_fields = ['name']

admin.site.register(Subcategory, SubcategoryAdmin)