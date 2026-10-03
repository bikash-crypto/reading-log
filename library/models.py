from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:author_detail', args=[self.pk])


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    class Status(models.TextChoices):
        WANT = 'want', 'Want to read'
        READING = 'reading', 'Reading now'
        FINISHED = 'finished', 'Finished'

    # Cloth colours for the book spines on the shelf page.
    class Cover(models.TextChoices):
        GREEN = 'green', 'Bottle green'
        NAVY = 'navy', 'Navy'
        OXBLOOD = 'oxblood', 'Oxblood'
        OCHRE = 'ochre', 'Ochre'
        SLATE = 'slate', 'Slate'
        PLUM = 'plum', 'Plum'

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre, blank=True, related_name='books')
    year_published = models.IntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=17, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WANT)
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1 to 5 stars. Leave empty until you have finished the book.',
    )
    cover = models.CharField(max_length=10, choices=Cover.choices, default=Cover.GREEN)
    started_on = models.DateField(null=True, blank=True)
    finished_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['author__name', 'year_published', 'title']

    def __str__(self):
        return f'{self.title} ({self.author})'

    def get_absolute_url(self):
        return reverse('library:book_detail', args=[self.pk])

    # --- helpers used by the templates -----------------------------------

    @property
    def stars(self):
        """Rating as a list of booleans, e.g. [True, True, True, False, False]."""
        if not self.rating:
            return []
        return [i < self.rating for i in range(5)]

    @property
    def spine_height(self):
        """Taller spine for longer books, kept between 225 and 290 px."""
        pages = self.pages or 250
        return max(225, min(290, 225 + pages // 10))

    @property
    def spine_width(self):
        """Thicker spine for longer books, kept between 32 and 62 px."""
        pages = self.pages or 250
        return max(32, min(62, 28 + pages // 20))
