# Generated by Django 3.2 on 2022-11-16 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20221116_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='billing_state',
            field=models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Goa', 'Goa'), ('Gujrat', 'Gujrat'), ('Assam', 'Assam'), ('Chhattisgarh', 'Chhattisgarh'), ('Bihar', 'Bihar'), ('Rajasthan', 'Rajasthan'), ('Punjab', 'Punjab'), ('Karnataka', 'Karnataka'), ('Manipur', 'Manipur')], max_length=100),
        ),
    ]
