from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=60, default='')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=60, default='')
    author = models.CharField(max_length=60, default='')
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(default='')
    publisher_id = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg'
        return url