from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics
from rest_framework import mixins
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.views import APIView, Response
from rest_framework import status


from app.models import Passport
from .serializers import PassportSerializer, LoginUserSerializer, UserSerializer



class PassportList(APIView):
    """
    List all passports, or create a new passport.
    """
    def get(self, request, format=None):
        passports = Passport.objects.all()
        serializer = PassportSerializer(passports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PassportSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassportViewSet(ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
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
