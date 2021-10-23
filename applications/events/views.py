import datetime

from applications.orders.models import Order
from applications.users.models import User
from applications.users.serializers import (AdminSerializer,
                                            InvitationSerializer)
from rest_framework import generics
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event, Event_Detail, Participants
from .serializers import (CRUD_DetailEventSerializer, DetailSerializer,
                          EventSerializer, PaginationSerializer,
                          RetrieveParticipantserializer, StatusSerializer)


class List_EventUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        idUser = self.request.user.id
        return Event.objects.events_by_user(idUser)


class List_DetailEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer

    def get_queryset(self):
        idEvent = self.kwargs['id']
        return Event_Detail.objects.filter(name=idEvent)


class ValidatePermissions(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        idEvent = self.kwargs['pk']
        idUser = self.request.user.id

        flag = True
        if Participants.objects.filter(name=idEvent, user_id=idUser, is_admin=True).exists():
            flag = False

        if flag:
            if Event.objects.filter(pk=idEvent, create_by=idUser).exists():
                flag = False

        return Response({'approved': flag})


class RetrieveStatus(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        idEvent = self.kwargs['pk']

        query = Event.objects.filter(pk=idEvent)

        return Response({'status': query[0].status, 'name': query[0].name})


class CreateDetail(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class UpdateDetail(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_DetailEventSerializer
    queryset = Event_Detail.objects.all()


class List_Events(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    pagination_class = PaginationSerializer

    def get_queryset(self):
        status = self.kwargs['status']
        return Event.objects.filter_events(status)


class RetrieveEvent(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class List_Detail(ListAPIView):
    serializer_class = DetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Event_Detail.objects.all()


class UpdateStatus(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatusSerializer
    queryset = Event.objects.all()


class RetrieveParticipants(ListAPIView):
    serializer_class = RetrieveParticipantserializer

    def get_queryset(self):
        idEvent = self.kwargs['pk']

        return Event.objects.filter(
            pk=idEvent
        )


class AssignPermissions(UpdateAPIView):
    serializer_class = AdminSerializer
    queryset = Event.objects.all()

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        # Recuperamos lista de id´s is_admin = True
        members = serializer.validated_data['members']

        # Agregar permisos de admin
        Participants.objects.filter(
            name=instance,
            user__in=members
        ).update(is_admin=True)

        # Quitar permisos de admin
        Participants.objects.filter(
            name=instance
        ).exclude(
            user__in=members
        ).update(is_admin=False)

        return Response({'response': 'ok'})


class AddParticipants(CreateAPIView):
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request,  *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Recuperar datos
        idEvent = serializer.validated_data['idEvent']
        listEmails = serializer.validated_data['listEmails']

        # Recuperar instancia del evento
        event_instance = Event.objects.get(id=idEvent)

        # Agregar participantes a la lista: list_members[]
        list_members = []
        # Agregamos la orden en blanco de cada participante list_orders[]
        list_orders = []

        # Agregar creador del evento
        if not str(self.request.user.email) in listEmails:
            listEmails.append(str(self.request.user.email))

        for email in listEmails:
            instance_member = User.objects.get(email=email)

            if not Order.objects.filter(event=idEvent, user_id=instance_member.id).exists():
                order = Order(
                    event=event_instance,
                    user=instance_member,
                    date=datetime.date.today()
                )
                list_orders.append(order)

            if not Participants.objects.filter(name=idEvent, user_id=instance_member.id).exists():
                participants = Participants(
                    name=event_instance,
                    user=instance_member,
                    is_admin=False
                )
                list_members.append(participants)

        # Insertamos list_members[]
        Participants.objects.bulk_create(list_members)

        # Insertamos list_orders[]
        Order.objects.bulk_create(list_orders)

        response = {
            'status': 'success',
        }

        return Response(response)
