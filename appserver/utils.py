import json

from django.utils import timezone



def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_group': [x.name for x in user.groups.all()]
    }