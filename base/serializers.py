from rest_framework.serializers import ModelSerializer
from base.models import UserProfile
from custom_accounts.models import User

class List_accounts_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']

class User_profile_Serializer(ModelSerializer):
    user = List_accounts_Serializer(many=False,read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','user','date','credits','free_credits']