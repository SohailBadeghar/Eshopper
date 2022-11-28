# Generated by Django 2.2.14 on 2022-11-07 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('status', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='products.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('coupon_code', models.CharField(max_length=10)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=100)),
                ('no_of_uses', models.IntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'PaymentGateway',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('name', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=255)),
                ('long_description', models.TextField(max_length=255)),
                ('price', models.FloatField(max_length=255)),
                ('special_price', models.FloatField(max_length=255)),
                ('special_price_from', models.DateField(auto_now=True)),
                ('special_price_to', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('quantity', models.IntegerField()),
                ('meta_title', models.TextField(max_length=100)),
                ('meta_description', models.TextField(max_length=100)),
                ('meta_keywords', models.TextField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product_Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Product_attributes',
            },
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('image', models.ImageField(upload_to='product')),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.Product')),
            ],
            options={
                'verbose_name_plural': 'productimages',
            },
        ),
        migrations.CreateModel(
            name='Product_Attributes_Values',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('attribute_value', models.CharField(blank=True, max_length=200, null=True)),
                ('product_attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes_values', to='products.Product_Attributes')),
            ],
            options={
                'verbose_name_plural': 'Product_attributes_values',
            },
        ),
        migrations.CreateModel(
            name='Product_Attributes_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes_details', to='products.Product')),
                ('product_attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes_details', to='products.Product_Attributes')),
                ('product_attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes_details', to='products.Product_Attributes_Values')),
            ],
            options={
                'verbose_name_plural': 'product_attributes_details',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='dj', max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(default='dj', max_length=255)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
