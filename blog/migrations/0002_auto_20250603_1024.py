from django.db import migrations

def create_categories(apps, schema_editor):
    Categorie = apps.get_model('blog', 'Categorie')
    categories = ['Sport', 'Technologie', 'Santé', 'Politique', 'Culture']
    for cat_name in categories:
        Categorie.objects.create(nom=cat_name)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),  # remplace par ta dernière migration précédente
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
