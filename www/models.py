from django.db import models

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.timestamp} - {self.text}"
    