from hashlib import sha1
from django.db import models
from .exception import Deupicated


class Image(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', width_field='width_image', height_field='height_image')
    alternative = models.CharField(max_length=50, blank=True, null=True)
    image_size = models.PositiveIntegerField(null=True, blank=True)
    image_hash = models.CharField(max_length=40, blank=True, null=True, db_index=True)
    width_image = models.PositiveIntegerField(blank=True, null=True, editable=False)
    height_image = models.PositiveIntegerField(blank=True, null=True ,editable=False)
    focal_point_x = models.PositiveIntegerField(blank=True, null=True)
    focal_point_y = models.PositiveIntegerField(blank=True , null=True)
    focal_point_width = models.PositiveIntegerField(blank=True, null=True)
    focal_point_height = models.PositiveIntegerField(blank=True , null=True)
    
    def images_hash(self):
        hasher = sha1()
        for chunk in self.image.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()
        
    def save(self):
        self.image_size = self.image.size
        self.image_hash = self.images_hash()
        if Image.objects.filter(image_hash=self.image_hash).exists():
            raise Deupicated('Image is elready exists')
        return super().save()
        