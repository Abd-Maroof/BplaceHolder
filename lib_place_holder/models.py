from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    year_publication = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    copies_total = models.PositiveIntegerField()
    copies_available = models.PositiveIntegerField()
    image_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.copies_available = self.copies_total
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BorrowingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    date_borrow = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(blank=True, null=True)
    date_return = models.DateTimeField(blank=True, null=True)
    returned_is = models.BooleanField(default=False)

    BORROW_DAYS = 14

    def borrow_book(self):
        if not self.date_due:
            self.date_due = self.date_borrow + timedelta(days=self.BORROW_DAYS)
            self.book.copies_available -= 1
            self.book.save()
            self.save()

    def return_book(self):
        self.date_return = timezone.now()
        self.book.copies_available += 1
        self.book.save()
        self.returned_is = True
        self.save()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
