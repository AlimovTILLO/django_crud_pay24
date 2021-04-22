from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics
from rest_framework import mixins
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.views import APIView, Response

from app.models import Passport
from .serializers import PassportSerializer, LoginUserSerializer, UserSerializer


class PassportViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()


class AddPassportViewSet(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def get_extra_actions():
        return []


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
