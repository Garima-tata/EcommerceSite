from django.db import models
# from django.utils.html import format_html 
# from django.contrib.auth.models import User #to get the user model

# ## category model 
# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  #foreign key linking to the user model
#     id_user = models.IntegerField()
#     profileimg = models.ImageField(upload_to='profile_images', default='defaultprofile.png')
#     location = models.CharField(max_length=100, blank=True) 
#     def __str__(self):
#         return self.user.username #return the username of the user note as user1 and user2 etc
