from django.contrib import admin
from .models import Department, Employee, CongeRequest, BulletinPaie, Prediction, Document, ModelePrediction

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(CongeRequest)
admin.site.register(BulletinPaie)
admin.site.register(Prediction)
admin.site.register(Document)
admin.site.register(ModelePrediction)
