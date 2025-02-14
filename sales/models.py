from django.db import models
from adminsortable.models import Sortable,SortableMixin

# Create your models here.
class Contact(SortableMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    company = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta(Sortable.Meta):
        ordering = ['the_order']

    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return f"Client: {self.email}"

    def __unicode__(self):
        return self.date
