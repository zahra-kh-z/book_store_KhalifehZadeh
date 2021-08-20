# Generated by Django 3.2.4 on 2021-08-16 23:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('New', 'جدید'), ('BestSeller', 'پرفروش')], max_length=12)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(default=0.0)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='picture/')),
                ('slug', models.SlugField(max_length=200)),
                ('available', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(default=0)),
                ('can_backorder', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'کتاب',
                'verbose_name_plural': 'کتاب ها',
                'ordering': ['label', '-create_date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کدهای تخفیف',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.IntegerField(default=0)),
                ('cont_new', models.IntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='books_inv', to='product.book')),
            ],
            options={
                'verbose_name': 'موجودی',
                'verbose_name_plural': 'موجودی ها',
                'ordering': ['count_use'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_discount', models.CharField(choices=[('Percent', 'درصدی'), ('Cash', 'نقدی')], max_length=12)),
                ('amount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('percent', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('max_use', models.IntegerField(verbose_name='Max number of items')),
                ('active', models.BooleanField(default=True)),
                ('book', models.ManyToManyField(related_name='book_off', to='product.Book')),
            ],
            options={
                'verbose_name': 'تخفیف',
                'verbose_name_plural': 'تخفیف ها',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='books_cat', to='product.Category'),
        ),
        migrations.AlterIndexTogether(
            name='book',
            index_together={('id', 'slug')},
        ),
    ]
