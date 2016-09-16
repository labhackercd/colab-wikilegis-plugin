from requests.exceptions import ConnectionError
from django.db.models.fields import DateTimeField
from django.db import IntegrityError
from colab.plugins.data import PluginDataImporter
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model
from colab_wikilegis import models
import requests
import urllib
import logging
import re

LOGGER = logging.getLogger('colab_wikilegis')
User = get_user_model()


class ColabWikilegisPluginDataImporter(PluginDataImporter):
    app_label = 'colab_wikilegis'

    def get_request_url(self, path, **kwargs):
        upstream = self.config.get('upstream')
        kwargs['api_key'] = self.config.get('api_key')
        params = urllib.urlencode(kwargs)

        if upstream[-1] == '/':
            upstream = upstream[:-1]

        return u'{}{}?{}'.format(upstream, path, params)

    def get_json_data(self, resource_name, page=1):
        api_url = '/api/{}/'.format(resource_name)
        url = self.get_request_url(api_url, page=page)
        full_json_data = []

        try:
            response = requests.get(url)
            json_data = response.json()
            full_json_data.extend(json_data['results'])
            if json_data['next']:
                page += 1
                json_page = self.get_json_data(resource_name, page)
                full_json_data.extend(json_page)
        except ConnectionError:
            pass
        except ValueError:
            pass

        return full_json_data

    def fill_object_data(self, model_class, data):
        try:
            obj = model_class.objects.get(id=data['id'])
        except model_class.DoesNotExist:
            obj = model_class()
        except KeyError:
            obj = model_class()

        for field in obj._meta.fields:
            try:
                if field.name == 'username':
                    obj.username = re.sub('@.*', '', data['email'])
                    continue

                if field.name == 'user':
                    user = User.objects.get(email=data['user']['email'])
                    obj.user = user
                    continue

                if field.name == 'author':
                    author = data['author']
                    print author
                    if author:
                        user = User.objects.get(email=author['email'])
                    else:
                        user = None
                    obj.author = user
                    continue

                if field.name == 'reporting_member':
                    reporting_member = data["reporting_member"]
                    if reporting_member:
                        user = User.objects.get(
                            email=reporting_member['email'])
                    else:
                        user = None
                    obj.user = user
                    continue

                if field.name == 'parent':
                    obj.parent_id = data['parent']
                    continue

                if field.name == 'replaced':
                    obj.replaced_id = data['replaced']
                    continue

                if field.name == 'type':
                    obj.type_id = data['type']
                    continue

                if field.name == 'bill':
                    obj.bill_id = data['bill']
                    continue

                if isinstance(field, DateTimeField):
                    value = parse_datetime(data[field.name])
                else:
                    value = data[field.name]

                setattr(obj, field.name, value)
            except KeyError:
                continue

        return obj

    def fetch_segment_types(self):
        json_data = self.get_json_data('segment_types')
        all_segment_types = []
        for data in json_data:
            segment_type = self.fill_object_data(models.WikilegisSegmentType,
                                                 data)
            segment_type.save()
            all_segment_types.append(segment_type.id)

        models.WikilegisSegmentType.objects.all().exclude(
            id__in=all_segment_types).delete()

    def fetch_bills(self):
        json_data = self.get_json_data('bills')
        all_bills = []
        for data in json_data:
            bill = self.fill_object_data(models.WikilegisBill, data)
            bill.save()
            all_bills.append(bill.id)

        models.WikilegisBill.objects.all().exclude(id__in=all_bills).delete()

    def fetch_segments(self):
        json_data = self.get_json_data('segments')
        retry_segments = []
        all_segments = []
        for data in json_data:
            segment = self.fill_object_data(models.WikilegisSegment, data)
            try:
                segment.save()
                all_segments.append(segment.id)
            except IntegrityError:
                retry_segments.append(segment)

        for segment in retry_segments:
            segment.save()
            all_segments.append(segment.id)

        models.WikilegisSegment.objects.all().exclude(
            id__in=all_segments).delete()

    def fetch_comments(self):
        json_data = self.get_json_data('comments')
        all_comments = []
        for data in json_data:
            comment = self.fill_object_data(models.WikilegisComment, data)
            comment.save()
            all_comments.append(comment.id)

        models.WikilegisComment.objects.all().exclude(
            id__in=all_comments).delete()

    def fetch_users(self):
        json_data = self.get_json_data('users')
        user_list = []
        for data in json_data:
            user = self.fill_object_data(User, data)
            user_list.append(user)
        return user_list

    def fetch_data(self):
        self.fetch_bills()
        self.fetch_segment_types()
        self.fetch_segments()
        self.fetch_comments()
