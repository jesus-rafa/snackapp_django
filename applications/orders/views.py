from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .functions import update_order
from .models import Order, OrderItem
from .serializers import (CRUD_OrderItemSerializer, OrderSerializer,
                          PaidOutSerializer)


class List_OrderEvent(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        idEvent = self.kwargs['id']

        return Order.objects.order_event(idEvent)


class List_OrderUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        idEvent = self.kwargs['idEvent']
        idUser = self.request.user.id

        return Order.objects.order_by_event_by_user(
            idEvent=idEvent,
            idUser=idUser
        )


class AddCart(CreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = CRUD_OrderItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = CRUD_OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        idOrder = str(serializer.validated_data['order'])

        instance_order = Order.objects.get(
            pk=idOrder
        )

        # agregamos al carrito
        OrderItem.objects.create(
            order=instance_order,
            product=serializer.validated_data['product'],
            description=serializer.validated_data['description'],
            price=serializer.validated_data['price'],
            quantity=serializer.validated_data['quantity'],
        )

        update_order(idOrder)

        return Response({'response': 'ok'})


class EditCart(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUD_OrderItemSerializer
    queryset = OrderItem.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        idOrder = str(serializer.validated_data['order'])

        serializer.save()

        update_order(idOrder)
        return Response({'response': 'ok'})


class EditPaid(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaidOutSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['amount_paid'] >= instance.amount:
            instance.paid_out = True
            instance.amount_paid = instance.amount
        else:
            instance.paid_out = False
            instance.amount_paid = serializer.validated_data['amount_paid']

        instance.save()

        return Response({'response': 'ok'})


class RemoveCart(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = CRUD_OrderItemSerializer
    queryset = OrderItem.objects.all()

    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        update_order(instance.order.pk)
