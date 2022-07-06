from rest_framework import serializers 
from .models import UserVisit
 
 
class UserActivitySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = UserVisit
        fields = ('id',
                  'user',
                  'remote_addr',
                  'ua_string',
                  'hash',
                  'session_key',
                  'created_at',
                  'timestamp',
                  'uuid')
