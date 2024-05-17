from rest_framework.serializers import ModelSerializer, CharField

from public.models import User


class UserSerializer(ModelSerializer):
    key = CharField(source="id", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        depth = 1
