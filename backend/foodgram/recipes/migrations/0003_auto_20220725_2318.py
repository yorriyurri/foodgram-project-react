# Generated by Django 3.2.14 on 2022-07-25 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220724_1856'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='favorite',
        ),
        migrations.RemoveConstraint(
            model_name='shoppingcart',
            name='shopping_cart',
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipeingredient'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
    ]
