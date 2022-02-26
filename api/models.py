from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    description= models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_deleted = models.BooleanField()
    
    def __str__(self):
        return f'Post ({self.id})'

LIKE = 'LIKE'
DISLIKE = 'DISLIKE'
STATUS = ((LIKE,'Like'), (DISLIKE,'Dislike') )

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=STATUS)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - Post ({self.post.id})'


    




