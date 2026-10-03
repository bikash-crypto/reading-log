# Reading log

A small Django web application for keeping track of the books you want to read, are reading and have finished. Books are shown as spines on a bookshelf: taller, thicker spines are longer books, and a red ribbon marks the ones you are reading now.

The project was made for the assignment *“15. Django web application”*, using AI to generate the models, the admin interface, the views and the templates.

## Submission details

- **Group name:** Ares
- **Members:** Bikash Bashyal, Biswash Pokhrel, Diwas Kharel.
- **Screenshots:** submitted with assignment.
- **GitHub repository:** https://github.com/bikash-crypto/reading-log
- **Agents and LLMs used:** Claude Opus 5.5

## What it does

- **Shelf** (`/`): every book as a spine on a wooden shelf, with a filter for *Want to read*, *Reading now* and *Finished*, and a search by title or author.
- **Book page**: cover, status, star rating, details, dates and your own notes.
- **Add, edit and remove books** with a form that checks the finish date is not before the start date.
- **Authors**: list of authors and a page for each with their books.
- **Admin** (`/admin/`): full management of authors, genres and books, with search, filters, inline editing of an author’s books and editable status and rating straight from the book list.

## Data model

| Model  | Fields |
|--------|--------|
| Author | name, birth year, country, bio |
| Genre  | name |
| Book   | title, author (foreign key), genres (many-to-many), year published, pages, ISBN, status, rating 1–5, spine colour, started on, finished on, notes, added at |

## Running it

You need Python 3.10 or newer. On Windows use `python` instead of `python3`.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install Django
pip install -r requirements.txt

# 3. Create the database tables
python3 manage.py migrate

# 4. (Optional) Fill the shelf with 19 sample books
python3 manage.py seed_books

# 5. Create an admin account
python3 manage.py createsuperuser

# 6. Start the development server
python3 manage.py runserver
```

Open http://127.0.0.1:8000/ for the app and http://127.0.0.1:8000/admin/ for the admin.

Run the tests with `python3 manage.py test library`.

## Project structure

```
mysite/                    project settings and root URLs
library/                   the app
  models.py                Author, Genre, Book
  admin.py                 admin interface
  forms.py                 BookForm with date validation
  views.py                 class-based views (list, detail, create, update, delete)
  urls.py                  app URLs
  templates/library/       HTML templates
  static/library/style.css stylesheet
  management/commands/seed_books.py   sample data
  tests.py                 tests for views and the form
```

## Secret key

`settings.py` reads the secret key from the `DJANGO_SECRET_KEY` environment variable so that a real key is never committed to GitHub. The fallback value only works for local development. Set `DJANGO_DEBUG=0` and a real key before deploying anywhere.

## How we built it with AI

1. Created the project and app by hand: `django-admin startproject mysite .` and `python3 manage.py startapp library`, then added `'library'` to `INSTALLED_APPS` in `settings.py`.
2. Described the data (books, authors, genres, reading status and rating) to the AI and got `models.py`.
3. Asked the AI for `admin.py`, ran `makemigrations`, `migrate` and `createsuperuser`, and tested the admin with `runserver`.
4. Asked the AI for views, URLs, templates and CSS for a public-facing site.

**Reflection: can AI create the views and templates, and how fast and easy was it?**
Yes. The AI generated the models, the admin interface, the views, URLs, templates and CSS, and they all worked on the first run. Writing the code took only minutes; most of our time went into setting things up on our own computer. We ran into two problems: we ran a command from the wrong folder, and one file was named manage.py.py instead of manage.py. We sent screenshots of the errors to the AI, and it explained how to fix them each time. Overall it took about almost 30min from start to finish. It was fast and easy, but we still needed basic knowledge of the command line and of how a Django project fits together (models = migrations = admin = views = URLs = templates). We learned the most when something went wrong and we had to understand why.
