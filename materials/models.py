from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage

# Custom User model
class User(AbstractUser):
    bio = models.TextField(blank=True)
    institution = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

# Category model
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

#  StudyMaterial model
class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='materials/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    preview_image = models.ImageField(upload_to='previews/', blank=True)

    def generate_preview(self):
        if self.file.name.endswith('.pdf'):
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(default_storage.open(self.file.name).read())
            if images:
                # Save first page as preview
                buffer = BytesIO()
                images[0].save(buffer, format='JPEG')
                self.preview_image.save(f'preview_{self.id}.jpg', ContentFile(buffer.getvalue()))

    def __str__(self):
        return self.title

#  Rating model
class Rating(models.Model):
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('material', 'user')

# Comment System
class Comment(models.Model):
    material = models.ForeignKey('StudYMaterial', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.material}'