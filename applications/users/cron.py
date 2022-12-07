from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Enviar_Correos

def generar_correos():
    print('ejecutando cron eventos...')

    # Obtener todos los correos que No se han enviado
    obj = Enviar_Correos.objects.filter(is_sent=False)

    # Enviar correos dependiendo del tipo
    for row in obj:
        if row.tipo == 'THANK':
            subject = 'Gracias por tu donacion'
            text_content = ''
            html_content = render_to_string(
                'users/email/thank.html',
                {'data': listEmails}
            )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                row.correo
            )
            msg.attach_alternative(html_content, "text/html")
            msg.mixed_subtype = 'related'
            msg.send()

        if row.tipo == 'CONTACT':
            subject = 'Contacto: ' + row.nombre
            text_content = ''
            html_content = render_to_string(
                'users/email/contact.html',
                {'contact': row.nombre, 'email': row.correo, 'message': row.comentarios}
            )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [row.correo, settings.EMAIL_HOST_USER]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if row.tipo == 'DELIVERED':
            event = Event.objects.filter(id=row.id_evento)

            # cargar adjuntos en el email
            if event[0].image:
                coupon_image = event[0].image
                img_data = coupon_image.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<coupon_image>')

            subject = 'Llego tu pedido: ' + event[0].name
            text_content = ''
            html_content = render_to_string(
                'users/email/delivered.html',
                {'data': event}
            )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                row.correo
            )

            msg.attach_alternative(html_content, "text/html")
            if event[0].image:
                msg.mixed_subtype = 'related'
                msg.attach(img)
            msg.send()

        if row.tipo == 'NEW':
            # Recuperar instancia del evento
            event = Event.objects.filter(id=idEvent)

            # cargar adjuntos en el email
            if event[0].image:
                coupon_image = event[0].image
                img_data = coupon_image.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<coupon_image>')

            subject = 'Invitacion a un Evento: ' + event[0].name
            text_content = ''
            html_content = render_to_string(
                'users/email/invitation_new.html',
                {'data': event, 'email': row.correo, 'password': row.password}
            )
            msg2 = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [row.correo]
            )
            msg2.attach_alternative(html_content, "text/html")
            if event[0].image:
                msg2.mixed_subtype = 'related'
                msg2.attach(img)
            msg2.send()


        if row.tipo == 'INVITATION':
            # Recuperar instancia del evento
            event = Event.objects.filter(id=idEvent)

            # cargar adjuntos en el email
            if event[0].image:
                coupon_image = event[0].image
                img_data = coupon_image.read()
                img = MIMEImage(img_data)
                img.add_header('Content-ID', '<coupon_image>')

            subject = 'Invitacion a un Evento: ' + event[0].name
            text_content = ''
            html_content = render_to_string(
                'users/email/invitations.html',
                {'data': event}
            )
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                row.correo
            )
            msg.attach_alternative(html_content, "text/html")
            if event[0].image:
                msg.mixed_subtype = 'related'
                msg.attach(img)
            msg.send()

    # Marcar correos como enviados
    Enviar_Correos.objects.filter(is_sent=False).update(is_sent=True)
