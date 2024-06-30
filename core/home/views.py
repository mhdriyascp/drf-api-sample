from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


from home.models import Person
from home.serializers import PersonSerializer, LoginSerializer, RegisterSerializer


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username= serializer.data['username'], password=serializer.data['password'])
            if not user:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"status": status.HTTP_200_OK, "token": str(token), "data": serializer.data, "message": "Login Successful"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterApi(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User Created Successfully", "data": serializer.data, "status": status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def index(request):
    """
        DRF API View
    """
    if request.method == 'GET':
        courses = {
            'course_name': 'Python Advanced Course',
            'learn': ['html', 'css', 'javascript', 'Django', 'flask'],
            'course_provider': 'MR'
        }
        return Response(courses)
    elif request.method == 'POST':
        return Response({'error': 'POST method not supported'})


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3
            paginator = Paginator(objs, page_size)
            serializer = PersonSerializer(paginator.page(page), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "Invalid Page", "status": status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        obj.delete()
        return Response({"message": "Deleted Successfully!", "status": status.HTTP_204_NO_CONTENT})


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    # http_method_names = ['get', 'post']

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)

        serializer = PersonSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data})

    @action(detail=False, methods=['post'])
    def send_mail_to_person(self, request):
        return Response({"message": "Send Mail Successfully!", "status": status.HTTP_200_OK})


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data
        return Response({"message": "Login Success!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull=False)
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        data = request.data
        obj = Person.objects.get(pk=data['id'])
        obj.delete()
        return Response({"message": "Deleted Successfully!", "status": status.HTTP_204_NO_CONTENT})



