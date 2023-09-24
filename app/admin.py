from django.contrib import admin
from app.models import Book, Members, Transaction

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['bookId','title','authors','isbn']
    list_filter = ['average_ratings', 'text_reviews_count']
    search_fields = ['bookId', 'title', 'authors', 'isbn', 'isbn13']

admin.site.register(Members)
admin.site.register(Transaction)