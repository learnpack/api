from django.db import models
from martor.models import MartorField

DRAFT = 'DRAFT'
PUBLISHED = 'PUBLISHED'
HIDDEN = 'HIDDEN'
QUESTION_STATUS = (
    (DRAFT, 'Draft'),
    (PUBLISHED, 'Published'),
    (HIDDEN, 'Hidden'),
)
# Create your models here.
class FAQQuestion(models.Model):
    slug = models.SlugField(max_length=150, primary_key=True)
    title = models.CharField(max_length=150)
    language = models.CharField(max_length=2, default='us')
    answer = MartorField(blank=True,null=True, default=None)
    status = models.CharField(max_length=15, choices=QUESTION_STATUS, default=DRAFT)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title
