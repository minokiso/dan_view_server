import os
import traceback
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from Utils.response import SuccessResponse, FailureResponse
from Utils.viewset import ModelViewSetPlus
from public.models import User


class UserViewSet(ModelViewSetPlus):
    model = User


class LoginView(TokenObtainPairView):
    # @create_log("登录")
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                request.user = serializer.user
                return SuccessResponse(data=serializer.validated_data)
            except TokenError as e:
                raise InvalidToken(e.args[0])

        except AuthenticationFailed as e:
            traceback.print_exc()
            return FailureResponse(err="Username or password is incorrect")
        except Exception as e:
            traceback.print_exc()
            return FailureResponse(err=str(e))
