from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'email')
    list_display = ('first_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')
    list_display = ('book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ('user', 'book', 'comment', 'stars_given')
    list_display = ('user', 'book')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
