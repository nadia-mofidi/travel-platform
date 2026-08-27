from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    subject=models.CharField(max_length=255,blank=True,null=True)
    massage=models.TextField()
    create_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)  
    class Meta:
        ordering=("create_date",)
    def __str__(self):
        return f"{self.id}-{self.name}"
    

class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email