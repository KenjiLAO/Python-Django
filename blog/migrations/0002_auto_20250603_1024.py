from django.db import migrations

def create_categories_and_tags(apps, schema_editor):
    # Création des catégories
    Categorie = apps.get_model('blog', 'Categorie')
    categories = ['Sport', 'Technologie', 'Santé', 'Politique', 'Culture']
    for cat_name in categories:
        Categorie.objects.create(nom=cat_name)

    # Création des tags
    Tag = apps.get_model('blog', 'Tag')
    tags = ['Django', 'Python', 'Web', 'Tutoriel', 'Sécurité']
    for tag_name in tags:
        Tag.objects.create(nom=tag_name)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories_and_tags),
    ]
