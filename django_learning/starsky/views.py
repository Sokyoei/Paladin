from django.shortcuts import render
from rest_framework import viewsets

from .models import BlackHole, Constellation, Galaxy, Nebula, Star
from .serializers import (
    BlackHoleSerializer,
    ConstellationSerializer,
    GalaxySerializer,
    NebulaSerializer,
    StarSerializer,
)


def index(request):
    return render(request, 'starsky/index.html')


class StarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer


class GalaxyViewSet(viewsets.ModelViewSet):
    queryset = Galaxy.objects.all()
    serializer_class = GalaxySerializer


class ConstellationViewSet(viewsets.ModelViewSet):
    queryset = Constellation.objects.all()
    serializer_class = ConstellationSerializer


class BlackHoleViewSet(viewsets.ModelViewSet):
    queryset = BlackHole.objects.all()
    serializer_class = BlackHoleSerializer


class NebulaViewSet(viewsets.ModelViewSet):
    queryset = Nebula.objects.all()
    serializer_class = NebulaSerializer
