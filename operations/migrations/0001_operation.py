# Generated by Django 3.2.6 on 2021-08-05 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=64)),
                ('operation_type', models.IntegerField(choices=[(1, 'Income'), (0, 'Outcome')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to='users.account', verbose_name='Operation')),
            ],
            options={
                'index_together': {('account_id', 'operation_type')},
            },
        ),
    ]