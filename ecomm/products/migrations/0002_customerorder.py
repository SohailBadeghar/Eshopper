# Generated by Django 2.2.14 on 2022-11-07 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('shipping_method', models.CharField(default='rail', max_length=50)),
                ('awb_no', models.CharField(default=uuid.uuid4, max_length=200)),
                ('transaction_id', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('grand_total', models.FloatField()),
                ('shipping_charges', models.FloatField(default=100)),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('billing_address_1', models.CharField(max_length=1024)),
                ('billing_address_2', models.CharField(max_length=100)),
                ('billing_state', models.CharField(max_length=100)),
                ('billing_city', models.CharField(max_length=100)),
                ('billing_zipcode', models.CharField(max_length=100)),
                ('shipping_address_1', models.CharField(max_length=1024)),
                ('shipping_address_2', models.CharField(max_length=100)),
                ('shipping_city', models.CharField(max_length=100)),
                ('shipping_state', models.CharField(max_length=100)),
                ('shipping_zipcode', models.CharField(max_length=100)),
                ('coupon', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon_used', to='products.Coupon')),
                ('payment_gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='products.PaymentGateway')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
