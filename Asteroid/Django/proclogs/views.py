from django.shortcuts import get_object_or_404
from asteroid.utils import expose

from proclogs.models import Proclog, AsteroidObs

@expose('proclogs/index.html')
def index(request):
    asteroids = AsteroidObs.objects.all()
    return dict(asteroids=asteroids)

@expose('proclogs/asteroid_info.html')
def asteroid_info(request, designated_name):
    aster = get_object_or_404(AsteroidObs, designated_name=designated_name)
    proclogs = Proclog.objects.filter(observation=aster)
    return dict(proclogs=proclogs, name=aster.object_name)
