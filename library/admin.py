from django.contrib import admin

from .models import Author, Book, Genre


class BookInline(admin.TabularInline):
    """Lets you see and edit an author's books on the author page."""
    model = Book
    fields = ('title', 'year_published', 'status', 'rating')
    extra = 0
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'birth_year', 'book_count')
    search_fields = ('name', 'country')
    inlines = [BookInline]

    @admin.display(description='Books')
    def book_count(self, obj):
        return obj.books.count()


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year_published', 'status', 'rating')
    list_filter = ('status', 'genres', 'rating')
    list_editable = ('status', 'rating')
    search_fields = ('title', 'author__name', 'isbn')
    autocomplete_fields = ('author',)
    filter_horizontal = ('genres',)
    fieldsets = (
        (None, {'fields': ('title', 'author', 'genres')}),
        ('Details', {'fields': ('year_published', 'pages', 'isbn', 'cover')}),
        ('My reading', {'fields': ('status', 'rating', 'started_on', 'finished_on', 'notes')}),
    )


admin.site.site_header = 'Reading log admin'
admin.site.site_title = 'Reading log admin'
admin.site.index_title = 'Manage books, authors and genres'
