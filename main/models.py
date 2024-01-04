from django.db import models

# Create your models here.

GENDER_CHOICES =(
    ("MALE","Male"),("FEMALE","Female"),("OTHER","Other"),
)

COLOR_CHOICES =(
    ("danger","Red"),("success","Green"),("into","Blue"),("warning","Yellow"),
)
ICON_CHOICES = (
    ('fa-solid fa-baseball-bat-ball', 'Cricket'),
    ('fa-solid fa-futbol', 'Football'),
    ('fa-solid fa-table-tennis-paddle-ball', 'Badminton'),
    ('fa-solid fa-person-biking', 'Cycle'),
    ('fa-solid fa-person-running', 'Running'),
    ('fa-solid fa-person-skiing-nordic', 'Skiing'),
    ('fa-solid fa-dumbbell', 'Fitness'),
)
STATUS_CHOICES =(
    ("Published","Published"),("Private","Private")
)

UNIT_CHOICES = (
    ('34x14', '34x14'),
    ('42x14', '42x14'),
    ('16x14', '16x14'),
)

class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)


class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.name)
    
