from django import forms

from .models import Book


RATING_CHOICES = [('', 'Not rated')] + [(n, '★' * n) for n in range(1, 6)]


class BookForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES, coerce=int, required=False, empty_value=None,
        help_text='Leave as “Not rated” until you finish the book.',
    )

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'genres',
            'year_published', 'pages', 'isbn', 'cover',
            'status', 'rating', 'started_on', 'finished_on', 'notes',
        ]
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'cover': forms.RadioSelect,
            'started_on': forms.DateInput(attrs={'type': 'date'}),
            'finished_on': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned = super().clean()
        started, finished = cleaned.get('started_on'), cleaned.get('finished_on')
        if started and finished and finished < started:
            self.add_error('finished_on', 'The finish date must be on or after the start date.')
        return cleaned
