from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    quote = models.TextField()
    tags = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
