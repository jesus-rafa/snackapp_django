from rest_framework import viewsets

from .models import Event, Event_Detail
from .serializers import (CRUD_DetailEventSerializer, CRUD_EventSerializer,
                          EventSerializer, PaginationSerializer)


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    pagination_class = PaginationSerializer


class CRUD_EventViewSet(viewsets.ModelViewSet):

    serializer_class = CRUD_EventSerializer
    queryset = Event.objects.all()


class CRUD_DetailEventViewSet(viewsets.ModelViewSet):

    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class EventUser_ViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def get_queryset(self):
        idUser = self.kwargs['id']
        return Event.objects.events_by_user(idUser)
