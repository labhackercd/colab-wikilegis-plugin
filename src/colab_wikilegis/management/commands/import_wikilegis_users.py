from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from colab_wikilegis.data_importer import ColabWikilegisPluginDataImporter
import uuid


User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        importer = ColabWikilegisPluginDataImporter()
        users = importer.fetch_users()
        for user in users:
            new_password = str(uuid.uuid4().get_hex()[0:10])
            print user.username, new_password
            user.set_password(new_password)
            new_user, created = User.objects.get_or_create(
                username=user.username,
                email=user.email,
            )
            new_user.set_password(new_password)
            new_user.is_active = True
            new_user.save()

            if created:
                self.send_email(new_user, new_password)

    def send_email(self, user, password):
        html = render_to_string('emails/wikilegis_new_user.html',
                                {'user': user, 'password': password})
        email_to = [user.email, ]
        subject = "Login no Novo Portal do e-Democracia"
        mail = EmailMultiAlternatives(subject=subject, to=email_to)
        mail.attach_alternative(html, 'text/html')
        mail.send()
