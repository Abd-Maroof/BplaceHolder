# lib_place_holder/admin.py
from django.contrib import admin
from .models import Author, Book, BorrowingRecord

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowingRecord)
