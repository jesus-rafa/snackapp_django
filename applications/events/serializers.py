from applications.users.models import User
from django.db.models import fields
from rest_framework import pagination, serializers

from .models import Event, Event_Detail, Participants


class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'get_initials',
            'avatar'
        )


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event_Detail
        fields = (
            'id',
            'name',
            'content',
            'image1',
            'image2',
            'file',
        )


class CRUD_EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'create_by',
            'date_start',
            'date_end',
            'hour_start',
            'hour_end',
            'status',
            'image',
        )


class CRUD_DetailEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event_Detail
        fields = (
            'id',
            'name',
            'content',
            'image1',
            'image2',
            'file',
        )


class EventSerializer(serializers.ModelSerializer):
    detail_event = DetailSerializer(many=True)
    create_by = UsersSerializers()

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'create_by',
            'date_start',
            'hour_start',
            'status',
            'image',
            'detail_event'
        )


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'status',
        )


class PaginationSerializer(pagination.PageNumberPagination):

    page_size = 6
    max_page_size = 50


class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'avatar',
            'get_full_name',
            'get_initials'
        )


class ParticipantshipSerializer(serializers.ModelSerializer):
    user = ParticipantsSerializer()

    class Meta:
        model = Participants
        fields = ('user', 'is_admin',)


class RetrieveParticipantserializer(serializers.ModelSerializer):
    participants = ParticipantshipSerializer(
        source='participants_event',
        many=True
    )

    class Meta:
        model = Event
        fields = (
            'id',
            'participants'
        )
