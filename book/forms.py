from django import forms
from .models import Book, Review, BorrowBook


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        self.book = kwargs.pop('book', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        user_purchased_or_borrowed = BorrowBook.objects.filter(
            user=self.user, book=self.book).exists()

        if not user_purchased_or_borrowed:
            raise forms.ValidationError(
                "You must purchase or borrow the book to leave a review.")

        return cleaned_data
