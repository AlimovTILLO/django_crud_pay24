from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import generics
from knox.models import AuthToken
from knox.auth import TokenAuthentication


from app.models import Passport
from .serializers import PassportSerializer, LoginUserSerializer, UserSerializer


class PassportViewSet(ModelViewSet):
    serializer_class = PassportSerializer
    queryset = Passport.objects.all()
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user":
            UserSerializer(user, context=self.get_serializer_context()).data,
            "token":
            AuthToken.objects.create(user)[1]
        })