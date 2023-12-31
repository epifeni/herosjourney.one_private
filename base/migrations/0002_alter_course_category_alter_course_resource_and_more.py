# Generated by Django 4.2.3 on 2023-11-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(blank=True, choices=[('computer-science', 'Computer Science'), ('data-science', 'Data science'), ('engineering', 'Engineering'), ('web-development', 'Web Development'), ('architecture', 'Architecture'), ('training', 'Training')], default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='course',
            name='resource',
            field=models.FileField(blank=True, null=True, upload_to='files/resource'),
        ),
        migrations.AlterField(
            model_name='course',
            name='sub_category',
            field=models.CharField(blank=True, choices=[('ml', 'Machine Learning'), ('data_science', 'Data Science'), ('python', 'Python'), ('javascript', 'JavaScript'), ('php', 'PHP'), ('django', 'Django'), ('html', 'HTML'), ('reactjs', 'React JS'), ('front-end', 'Front-End'), ('back-end', 'Back-End'), ('running', 'Running'), ('gym', 'GYM')], default='', max_length=255, null=True),
        ),
    ]
