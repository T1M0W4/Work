from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VinylRecord(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    audio_file = models.FileField(upload_to='vinyl_audio/')
    tags = models.ManyToManyField(Tag, related_name='records')

    def __str__(self):
        return f"{self.title} - {self.artist}"