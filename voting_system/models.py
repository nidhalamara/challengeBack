from django.db import models

from authenticator.models import VUser


class Vote(models.Model):
    v_user = models.ForeignKey(VUser, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='votes', null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    comment = models.TextField( null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)


from django.core.validators import FileExtensionValidator
from django.db import models

class Document(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    document = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])]
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    proposition = models.ForeignKey('Proposition', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete()
        super().delete(*args, **kwargs)

