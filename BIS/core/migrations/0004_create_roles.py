from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model('core', 'Role')
    Role.objects.get_or_create(name='CPDMO Staff')
    Role.objects.get_or_create(name='CPDMO Chief')
    Role.objects.get_or_create(name='System Administrator')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_password'),  # Replace with the actual dependency
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]
