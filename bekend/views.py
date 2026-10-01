from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# views.py faylida

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset

class RegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        again_password = request.data.get('again_password')

        if not username or not email or not password or not again_password:
            return Response(
                {'error': "Barcha maydonlar to'ldirilishi shart!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != again_password:
            return Response(
                {'error': "Parollar bir xil emas!"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'username': 'Bu foydalanuvchi nomi band!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'email': 'Bu email allaqachon ishlatilgan!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        User.objects.create_user(username=username, email=email, password=password)
        return Response(
            {'message': "Muvaffaqiyatli ro'yxatdan o'tildi!"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response(
                {'message': 'Muvaffaqiyatli kirdingiz!'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': "Foydalanuvchi nomi yoki parol noto'g'ri!"},
                status=status.HTTP_400_BAD_REQUEST,
            )