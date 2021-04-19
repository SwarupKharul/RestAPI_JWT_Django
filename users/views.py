from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, ProfileSerializer
from .models import NewUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions


class ProfileEditPermission(BasePermission):
    message = 'Editing profile is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        print(request.user)
        return obj == request.user or request.user.is_staff

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileList(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = ProfileSerializer




class Profile(generics.RetrieveUpdateDestroyAPIView, ProfileEditPermission):
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    serializer_class = ProfileSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     # There is nothing to validate or save here. Instead, we just want the
    #     # serializer to handle turning our `User` object into something that
    #     # can be JSONified and sent to the client.
    #     serializer = self.serializer_class(request.user)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     serializer_data = request.data.get('user', {})

    #     # Here is that serialize, validate, save pattern we talked about
    #     # before.
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)

