# views.py
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from .mixins import PlatformApiCallMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import *
from rest_framework import status
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .decorators import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import  TokenAuthentication


class RegisterUser(APIView):
    permission_classes = [AllowAny]  # Exempt this view from authentication

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'something is wrong'})
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({'status': 200, 'payload': serializer.data, 'token': token_obj.key, 'message': 'your data is saved'})


class ProductViewSet(PlatformApiCallMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'amount']

    def perform_create(self, serializer):
        if Product.objects.filter(name=serializer.validated_data['name']).exists():
            raise serializers.ValidationError('Product with this name already exists.')
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            self.record_api_call(request)
            return response
        except serializers.ValidationError as e:
            return Response({'status': 400, 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.record_api_call(request)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.record_api_call(request)
        return response



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer', 'seller').prefetch_related('products')
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['products__name']
    search_fields = ['products__name']
    ordering_fields = ['amount', 'id']
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_5(self, request):
        queryset = self.filter_queryset(self.get_queryset())[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @restrict_to_owner
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Ensure user doesn't already have a seller profile
        if Seller.objects.filter(user=request.user).exists():
            return Response({"error": "Seller profile already exists for this user."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

