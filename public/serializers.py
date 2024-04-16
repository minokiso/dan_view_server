from rest_framework.serializers import ModelSerializer, CharField

from public.models import User, Test


class TestSerializer(ModelSerializer):
    key = CharField(source="id", read_only=True)

    class Meta:
        model = Test
        fields = "__all__"


class UserSerializer(ModelSerializer):
    test = TestSerializer(many=True, read_only=True, )
    key = CharField(source="id", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        depth = 1
