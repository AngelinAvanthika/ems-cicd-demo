from django.shortcuts import render
from .models import Employee,Department,Project,User,UserDetails
from .serializers import EmployeeSerializer,DepartmentSerializer,ProjectSerializer,UserDetailsSerializer,UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate

# Create your views here.
#EmployeeViewSet-->class name
#viewsets.ModelViewSet-->DRF class that provides implementations for CRUD operations
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=["EmployeeName","Designation"]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset=UserDetails.objects.all()
    serializer_class=UserDetailsSerializer

class SignupAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return Response({
                "user_id":user.id,
                "user_name":user.username,
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "role":user.groups.all()[0].id if user.groups.exists() else None
            },status=status.HTTP_201_CREATED)
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request, username=username, password=password)
            if user is not None:
                refresh=RefreshToken.for_user(user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    "role":user.groups.all()[0].id if user.groups.exists() else None
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid email or password"
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        response={
            "status":status.HTTP_400_BAD_REQUEST,
            "message":"BAD REQUEST",
            "data":serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)