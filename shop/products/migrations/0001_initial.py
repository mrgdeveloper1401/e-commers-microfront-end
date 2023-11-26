# Generated by Django 4.2.7 on 2023-11-26 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('images', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('types', models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=12)),
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OptionGroupValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='products.optiongroup')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('structure', models.CharField(choices=[('standalone', 'Standalone'), ('parent', 'Parent'), ('child', 'Child')], default='standalone', max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('upc', models.CharField(blank=True, max_length=24, null=True)),
                ('sku', models.CharField(blank=True, max_length=13, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('meta_title', models.CharField(blank=True, max_length=128, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('types', models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('option', 'Option'), ('multi_option', 'Multi Option')], default='text', max_length=12)),
                ('required', models.BooleanField(default=False)),
                ('option_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.optiongroup')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRecomendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(default=0)),
                ('primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='products.product')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_recomendation', to='products.product')),
            ],
            options={
                'ordering': ('primary', '-rank'),
                'unique_together': {('primary', 'recommendation')},
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='images.image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_images', to='products.product')),
            ],
            options={
                'ordering': ('display_order',),
            },
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_stock', models.BooleanField(default=True)),
                ('requires_shipping', models.BooleanField(default=True)),
                ('options', models.ManyToManyField(blank=True, to='products.option')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True)),
                ('value_integer', models.IntegerField(blank=True, null=True)),
                ('value_float', models.FloatField(blank=True, null=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productattribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('value_multi_option', models.ManyToManyField(related_name='value_multi_options', to='products.optiongroupvalue')),
                ('value_option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.optiongroupvalue')),
            ],
            options={
                'unique_together': {('product', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='products.productclass'),
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(through='products.ProductAttributeValue', to='products.productattribute'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='category_products', to='category.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.productclass'),
        ),
        migrations.AddField(
            model_name='product',
            name='recommender_system',
            field=models.ManyToManyField(through='products.ProductRecomendation', to='products.product'),
        ),
    ]
