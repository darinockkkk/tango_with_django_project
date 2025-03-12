from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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

    # django will display the string representation of the object, derived from __str__().
    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    # required line, links UserProfile to a User model instance
    # one-to-one relationship between custom user profile model and Django’s built-in User model
    # if linked User is deleted, this profile will also be deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True) # all profile images stored in tango_with_django_project/media/profile_images/
    
    # return meaningful value when string representation of UserProfile model instance is requested
    # without __str__, profile would return something like <UserProfile object (1)>, but this method makes it human-readable by showing username
    def __str__(self):
        return self.user.username

