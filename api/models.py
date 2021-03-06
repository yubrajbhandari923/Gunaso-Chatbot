from django.db import models
from fb_services.FBAPI import getLatLong

def _(s):
    return s


class GptBot(models.Model):

    prompt = models.TextField(_("Prompt"), blank=True, null=True)
    psid = models.IntegerField(_("psID"))
    is_address = models.BooleanField(_("is_address"), default=False)
    service_id = models.IntegerField(_("service_id"), default=0)
    class Meta:
        verbose_name = _("GptBot")
        verbose_name_plural = _("GptBots")

    def get_absolute_url(self):
        return reverse("GptBot_detail", kwargs={"pk": self.pk})

class Ambulance(models.Model):

    name = models.CharField( max_length=1000)
    description = models.TextField(blank=True, null=True)
    hospital_name = models.CharField(_("Hospital Name"), max_length=1000, blank=True, null=True)
    phone = models.CharField(_("Phone No."), max_length=20)
    image = models.ImageField(_("Image"), upload_to='ambulances', width_field=None, max_length=None, blank=True, null=True)    

    class Meta:
        verbose_name = _("Ambulance")
        verbose_name_plural = _("Ambulances")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Ambulance_detail", kwargs={"pk": self.pk})

class Hospital(models.Model):

    name = models.CharField( max_length=1000)
    address = models.TextField(_("Address"), blank=True, null=True)

    class Meta:
        verbose_name = _("hospital")
        verbose_name_plural = _("hospitals")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hospital_detail", kwargs={"pk": self.pk})
    
    @property
    def latlong(self):
        return getLatLong(self.address)
class Doctor(models.Model):

    """ {"id":"13332","name":"Dr. Subodh Dahal","description":"Psychiatry and Mental Health ","slug":"dr-subodh-dahal","image":"http://www.hamrodoctor.com/image.php?src=/uploads/doctors/5d56cc05a4143.jpeg&w=350&h=350","nmc":" 10858","hospitals":[{"name":"Dr. Iwamura Memorial Hospital & Research Center","location":"Sallaghari Ukalo, Bhaktapur"},{"name":"SHANKHAMUL HEALTHCARE","location":"Shankhamul, KMC - 10, Kathmandu"}]} """

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("description"))

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Doctor_detail", kwargs={"pk": self.pk})

class DisasterRelif(models.Model):

    name = models.CharField(_("Name"), max_length=1000)
    phone = models.CharField(_("Phone Number"), max_length=100)
    address = models.CharField(_("Address"), max_length=500)

    class Meta:
        verbose_name = _("DisasterRelif")
        verbose_name_plural = _("DisasterRelifs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DisasterRelif_detail", kwargs={"pk": self.pk})

class Violence(models.Model):

    
    name = models.CharField(_("Name"), max_length=1000)
    phone = models.CharField(_("Phone Number"), max_length=100)
    address = models.CharField(_("Address"), max_length=500)


    class Meta:
        verbose_name = _("Violence")
        verbose_name_plural = _("Violences")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Violence_detail", kwargs={"pk": self.pk})
