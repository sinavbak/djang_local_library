from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 200, help_text ="Blog başlığını girin")
    subtitle = models.TextField(help_text="Alt Başlık")
    #author = models.ForeignKey('author',on_delete = models.SET_NULL,null=True)
    #category = models.ForeignKey('category',on_delete = models.SET_NULL,null=True)
    content = models.TextField(help_text="İçeriği girin")
    #create_date = models.Da