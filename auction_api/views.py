from django.utils import timezone
from django.core.cache import cache
from .models import User, Product, Bid
from .serializers import UserSerializer, ProductSerializer, BidSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
import os
import yagmail
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class BidCreateAPIView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):

        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        amount = serializer.validated_data['amount']


        start_time = timezone.localtime(product.start_time)

        if timezone.now() < start_time:
            return Response({'error': f'Auction is not open yet. Please wait until {product.start_time}.', 'start_time': product.start_time}, status=status.HTTP_400_BAD_REQUEST)


        time_difference = timezone.now() - product.last_bid_time
        if time_difference > timezone.timedelta(minutes=1):
            product.status = 'closed'
            product.save()

            result(product)

            return Response({'error': 'Auction closed. No further bids accepted.'}, status=status.HTTP_400_BAD_REQUEST)


        product.last_bid_time = timezone.now()
        product.save()

        try:
            Bid.place_bid(user, product, amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)





def result(product):
    winning_bid = Bid.objects.filter(product=product).order_by('-amount').first()
    if winning_bid:
        winning_bidder = winning_bid.user
        receiver_email = winning_bidder.email
        sender = 'jemal.kobakhidze.1@btu.edu.ge'
        subject = "You are winner"
        content = f"Congratulations! You won the auction for {product.name}."

        yag = yagmail.SMTP(user=sender, password=os.getenv('EMAIL_PASSWORD'))
        yag.send(to=receiver_email, subject=subject, contents=content)