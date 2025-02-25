from django.db import migrations


def add_common_genres(apps, schema_editor):
    Genre = apps.get_model("libro", "Genre")
    genres = [
        {
            "name": "Fiction",
            "description": "Literature in the form of prose that describes imaginary events and people",
        },
        {
            "name": "Non-fiction",
            "description": "Writing that is based on facts, real events, and real people",
        },
        {
            "name": "Mystery",
            "description": "Fiction dealing with the solution of a crime or the revealing of secrets",
        },
        {
            "name": "Science Fiction",
            "description": "Fiction based on imagined future scientific or technological advances",
        },
        {
            "name": "Fantasy",
            "description": "Fiction featuring magical and supernatural elements",
        },
        {
            "name": "Romance",
            "description": "Fiction focusing on romantic love relationships",
        },
        {
            "name": "Thriller",
            "description": "Fiction characterized by suspense and excitement",
        },
        {
            "name": "Horror",
            "description": "Fiction intended to scare, unsettle, or horrify the reader",
        },
        {
            "name": "Historical Fiction",
            "description": "Fiction set in the past, often during significant historical events",
        },
        {
            "name": "Biography",
            "description": "Non-fiction narrative of a person's life",
        },
        {
            "name": "Self-help",
            "description": "Books aimed at personal development and improvement",
        },
        {
            "name": "Poetry",
            "description": "Literary work in which special intensity is given to the expression of feelings and ideas",
        },
    ]

    for genre_data in genres:
        Genre.objects.get_or_create(
            name=genre_data["name"], defaults={"description": genre_data["description"]}
        )


def remove_common_genres(apps, schema_editor):
    Genre = apps.get_model("libro", "Genre")
    Genre.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "libro",
            "0002_author_alter_book_author",
        ),
    ]

    operations = [
        migrations.RunPython(add_common_genres, remove_common_genres),
    ]
