from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category Name')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Subcategory Name')
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False,
                                        verbose_name='Parent Category Name')

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=50, verbose_name='Movie Name')
    director = models.CharField(max_length=50, verbose_name='Director')
    category = models.ManyToManyField(Category, null=False, blank=False, verbose_name='Category Name')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='Publish Date')
    banner = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
