from django.db import models

# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
    )
    place = models.CharField(
        max_length=120,
    )
    message = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.full_name())

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
