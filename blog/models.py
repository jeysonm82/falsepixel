from django.db import models

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    pub_date = models.DateField()
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def preview(self):
        return self.content[1:min(len(self.content), 100)]
    

class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=400)
    is_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s says %s"%(self.author, self.content[1:min(len(self.content), 100)])


"""
class Tag(models.Model):
    pass
"""
