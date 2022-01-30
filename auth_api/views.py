from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from accounts.models import UserProfile


# Create your views here.

@api_view(('GET', 'POST'))
def api_root(request, format=None):
    return Response(
        {
            'login': reverse('api-login', request=request, format=format),
            'register': reverse('api-register', request=request, format=format),
            'logout': reverse('api-logout', request=request, format=format),
            'test': reverse('api-test', request=request, format=format)
        }
    )


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class LoginViewApi(ObtainAuthToken):
    pass


class RegisterViewApi(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.user.auth_token)
        self.request.user.auth_token.delete()
        return Response({'Message': 'Logout successful'}, status=status.HTTP_200_OK)
