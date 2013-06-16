from django.db import models

class Test(models.Model):
    """
    Model of test attributes.
    """
    id=models.AutoField(primary_key=True)
    path=models.CharField(max_length=100)

    def __unicode__(self):
        return self.path
