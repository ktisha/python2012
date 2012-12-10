from django.db import models
from django.utils.translation import ugettext_lazy as _

class Proclog(models.Model):

    observation = models.ForeignKey("AsteroidObs")

    #    photo = models.ImageField(upload_to="places", default=None)

    pclg_image_name = models.CharField(_("Image name"), max_length = 80)
    pclg_exposure = models.CharField(_("Exposure"), max_length = 32)
    pclg_CCD_temp = models.CharField(_("CCD temperature"), max_length = 32)
    pclg_filter = models.CharField(_("Filter"), max_length = 32)
    pclg_exp_time = models.CharField(_("Mid-exposure time"), max_length = 32)
    pclg_latitude = models.CharField(_("Latitude"), max_length = 32)
    pclg_longitude = models.CharField(_("Longitude"), max_length = 32)
    pclg_altitude = models.CharField(_("Altitude"), max_length = 32)
    pclg_catalog_astrometric = models.CharField(_("Astrometric catalog"), max_length = 32)
    pclg_image_center_RA = models.CharField(_("Image center RA"), max_length = 32)
    pclg_image_center_DEC = models.CharField(_("Image center DEC"), max_length = 32)

    def __unicode__(self):
        return self.pclg_image_name

class AsteroidObs(models.Model):
    object_name = models.CharField(_("Object Name"), max_length = 32)
    designated_name = models.CharField(_("Short Object Name"), max_length = 32)
    # description = models.TextField(...)

    def __unicode__(self):
        return self.designated_name
