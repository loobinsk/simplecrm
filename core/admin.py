from django.contrib import admin
from .models import Client, Call, CallComment, SelectedData
import csv
import datetime
from django.http import HttpResponse

admin.site.register(Client)
admin.site.register(Call)
admin.site.register(CallComment)
admin.site.register(SelectedData)
