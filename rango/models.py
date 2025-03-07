from django.db import models
from django.template.defaultfilters import slugify

# here Django will create tables in the underlying database

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    # call the slugify() function and update the new slug field with it
    def save(self, *args, **kwargs):
        # slug field is set by using the output of the slugify() as the new field’s value
        self.slug = slugify(self.name)

        # overriden save() method then calls the parent save() method
        # to save the changes to the correct database table.
        super(Category, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    # Django will display the string representation of the object, derived from __str__().
    def __str__(self):
        return self.title
