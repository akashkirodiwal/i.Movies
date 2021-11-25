from django.db import models
from django.db.models import CheckConstraint, Q, F


# Create your models here.

class Movie(models.Model):
    
    rating_choice = (
        ('U', 'U'),
        ('UA', 'U/A'),
        ('A', 'A'),
        ('R', 'R'),
    )
    title = models.CharField(max_length=256)
    description = models.TextField()
    cast = models.CharField(max_length=1024)
    duration_min = models.IntegerField()
    certification_label = models.CharField(max_length=2,choices=rating_choice)

    def __str__(self):
        return self.title


class Theatre(models.Model):
    city_choice=(
        ('DELHI','Delhi'),
        ('KOLKATA','Kolkata'),
        ('MUMBAI','Mumbai'),
        ('CHENNAI','Chennai'),
        ('BANGALORE','Bangalore'),
        ('HYDERABAD','Hyderabad'),
    )
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=9,choices=city_choice,default="",editable=True)

    def __str__(self):
        return self.name + '-' +self.city


class Screening(models.Model):
    hall_name = models.CharField(max_length=32)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre_id = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    available_seats = models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    time=models.DateTimeField(auto_now=False)
    
    def __str__(self):
        return self.theatre_id.name + ' - ' +' - '+ self.movie_id.title + ' - ' + self.hall_name + ' - ' +str(self.price)
