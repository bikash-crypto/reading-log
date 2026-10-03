"""Fill the database with sample books so the shelf has something on it.

Usage:  python3 manage.py seed_books
Safe to run more than once: existing books are skipped.
"""
from datetime import date

from django.core.management.base import BaseCommand

from library.models import Author, Book, Genre

AUTHORS = {
    'Ursula K. Le Guin': ('USA', 1929, 'Wrote science fiction and fantasy that treats invented worlds as serious thought experiments about society, gender and power.'),
    'Kazuo Ishiguro': ('United Kingdom', 1954, 'Novelist known for quiet, unreliable narrators looking back on lives they only half understand. Nobel Prize in Literature, 2017.'),
    'Toni Morrison': ('USA', 1931, 'Novelist and editor whose books centre Black American history and memory. Nobel Prize in Literature, 1993.'),
    'Gabriel García Márquez': ('Colombia', 1927, 'Journalist and novelist, the best-known voice of Latin American magical realism. Nobel Prize in Literature, 1982.'),
    'Mary Shelley': ('United Kingdom', 1797, 'Wrote Frankenstein as a teenager, often called the first science fiction novel.'),
    'Fyodor Dostoevsky': ('Russia', 1821, 'Nineteenth-century novelist of guilt, faith and psychology.'),
    'Haruki Murakami': ('Japan', 1949, 'Novelist whose ordinary narrators drift into dreamlike, uncanny situations.'),
    'Virginia Woolf': ('United Kingdom', 1882, 'Modernist novelist and essayist who followed the flow of her characters’ thoughts.'),
    'Octavia E. Butler': ('USA', 1947, 'Science fiction writer focused on power, survival and change.'),
    'Italo Calvino': ('Italy', 1923, 'Playful, inventive writer of fables, puzzles and short fiction.'),
}

# title, author, year, pages, genres, status, rating, cover, started, finished, notes
BOOKS = [
    ('A Wizard of Earthsea', 'Ursula K. Le Guin', 1968, 183, ['Fantasy'], 'finished', 5, 'navy', date(2026, 1, 3), date(2026, 1, 9), 'The shadow is such a simple idea and it still works perfectly.'),
    ('The Left Hand of Darkness', 'Ursula K. Le Guin', 1969, 304, ['Science fiction'], 'finished', 4, 'slate', date(2026, 2, 1), date(2026, 2, 20), 'The ice crossing is the best part.'),
    ('The Dispossessed', 'Ursula K. Le Guin', 1974, 387, ['Science fiction'], 'want', None, 'ochre', None, None, ''),
    ('The Remains of the Day', 'Kazuo Ishiguro', 1989, 258, ['Literary fiction'], 'finished', 5, 'green', date(2026, 3, 2), date(2026, 3, 12), 'Everything important happens in what Stevens refuses to say.'),
    ('Never Let Me Go', 'Kazuo Ishiguro', 2005, 288, ['Literary fiction', 'Science fiction'], 'finished', 4, 'slate', date(2026, 4, 5), date(2026, 4, 18), ''),
    ('Klara and the Sun', 'Kazuo Ishiguro', 2021, 303, ['Literary fiction', 'Science fiction'], 'reading', None, 'ochre', date(2026, 9, 20), None, 'Halfway. Klara’s way of seeing the world in boxes is lovely.'),
    ('Beloved', 'Toni Morrison', 1987, 324, ['Literary fiction'], 'want', None, 'oxblood', None, None, ''),
    ('Song of Solomon', 'Toni Morrison', 1977, 337, ['Literary fiction'], 'finished', 5, 'plum', date(2025, 11, 2), date(2025, 11, 25), ''),
    ('One Hundred Years of Solitude', 'Gabriel García Márquez', 1967, 417, ['Magical realism', 'Classic'], 'finished', 5, 'ochre', date(2025, 7, 1), date(2025, 7, 30), 'Keep a family tree next to you while reading.'),
    ('Chronicle of a Death Foretold', 'Gabriel García Márquez', 1981, 120, ['Magical realism'], 'want', None, 'green', None, None, ''),
    ('Frankenstein', 'Mary Shelley', 1818, 280, ['Gothic', 'Classic', 'Science fiction'], 'finished', 4, 'oxblood', date(2025, 10, 20), date(2025, 10, 31), 'Read it for Halloween. The creature is far more eloquent than the films suggest.'),
    ('Crime and Punishment', 'Fyodor Dostoevsky', 1866, 671, ['Classic', 'Literary fiction'], 'reading', None, 'oxblood', date(2026, 8, 15), None, 'Slow going, but Porfiry’s interviews are worth it.'),
    ('Norwegian Wood', 'Haruki Murakami', 1987, 296, ['Literary fiction'], 'finished', 3, 'green', date(2025, 6, 2), date(2025, 6, 14), ''),
    ('Kafka on the Shore', 'Haruki Murakami', 2002, 467, ['Magical realism'], 'want', None, 'navy', None, None, ''),
    ('Mrs Dalloway', 'Virginia Woolf', 1925, 194, ['Classic', 'Literary fiction'], 'finished', 4, 'plum', date(2026, 5, 10), date(2026, 5, 16), ''),
    ('To the Lighthouse', 'Virginia Woolf', 1927, 209, ['Classic', 'Literary fiction'], 'want', None, 'slate', None, None, ''),
    ('Kindred', 'Octavia E. Butler', 1979, 264, ['Science fiction'], 'finished', 5, 'navy', date(2026, 6, 1), date(2026, 6, 8), 'Could not put it down.'),
    ('Parable of the Sower', 'Octavia E. Butler', 1993, 345, ['Science fiction'], 'want', None, 'oxblood', None, None, ''),
    ('Invisible Cities', 'Italo Calvino', 1972, 165, ['Fantasy', 'Literary fiction'], 'finished', 4, 'plum', date(2026, 7, 4), date(2026, 7, 7), 'Best read a few cities at a time.'),
]


class Command(BaseCommand):
    help = 'Adds sample authors, genres and books.'

    def handle(self, *args, **options):
        authors = {}
        for name, (country, born, bio) in AUTHORS.items():
            authors[name], _ = Author.objects.get_or_create(
                name=name, defaults={'country': country, 'birth_year': born, 'bio': bio},
            )

        added = 0
        for title, author, year, pages, genres, status, rating, cover, started, finished, notes in BOOKS:
            book, created = Book.objects.get_or_create(
                title=title,
                author=authors[author],
                defaults={
                    'year_published': year, 'pages': pages, 'status': status,
                    'rating': rating, 'cover': cover, 'started_on': started,
                    'finished_on': finished, 'notes': notes,
                },
            )
            if created:
                book.genres.set(Genre.objects.get_or_create(name=g)[0] for g in genres)
                added += 1

        self.stdout.write(self.style.SUCCESS(f'Added {added} books ({Book.objects.count()} in total).'))
