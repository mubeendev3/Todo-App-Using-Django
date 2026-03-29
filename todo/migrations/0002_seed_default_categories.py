# Generated manually — seed categories so task form dropdown has options

from django.db import migrations


DEFAULT_NAMES = ('Work', 'Personal', 'Shopping', 'Study', 'Health', 'Other')


def seed_categories(apps, schema_editor):
    Category = apps.get_model('todo', 'Category')
    if Category.objects.exists():
        return
    Category.objects.bulk_create(
        [Category(name=name) for name in DEFAULT_NAMES]
    )


def unseed_categories(apps, schema_editor):
    Category = apps.get_model('todo', 'Category')
    Category.objects.filter(name__in=DEFAULT_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
