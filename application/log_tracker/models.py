from django.db import models
from .validators import validate_log_level
class Log(models.Model):
    level         = models.CharField(max_length=10,null=False,blank=False,validators=[validate_log_level])
    log_date_time = models.DateTimeField()
    message       = models.CharField(max_length=4096,blank=True)

    def __str__(self):
        return f'{self.log_date_time} - {self.level} - {self.message[:50]}'