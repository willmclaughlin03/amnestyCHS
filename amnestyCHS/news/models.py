from django.db import models
from django.utils.text import slugify
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique = True, bland = True) # Slug field for URL
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # Generate slug from title
        super().save(*args, **kwargs) 
         
    def __str__(self):
        return self.title