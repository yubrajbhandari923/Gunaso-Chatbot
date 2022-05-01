from django.contrib import admin
from api.models import GptBot, Ambulance, Doctor, Hospital, DisasterRelif, Violence 
# Register your models here.
admin.site.register(GptBot)
admin.site.register(Doctor)
admin.site.register(Ambulance)
admin.site.register(Hospital)
admin.site.register(DisasterRelif)
admin.site.register(Violence)