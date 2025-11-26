from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from order.models import Order
from .serializer import AdminOrderSerializer

class AdminOrderPAgination(PageNumberPagination):
    page_size=10
    page_size_query_param="page_size"
    max_page=100
class AdminOrderListView(ListAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=AdminOrderSerializer
    pagination_class=AdminOrderPAgination

    def get_queryset(self):
        queryset = Order.objects.select_related("user").prefetch_related("items__product").order_by("-id")
        # Search (username,product name) 
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(user__username__icontains=search) |
                
                Q(name__icontains=search) |
                Q(items__product__name__icontains=search)
            ).distinct()

        return queryset

class AdminStatusUpdateView(APIView):
    permission_classes=[IsAdminUser]
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if not new_status:
            return Response({"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()

        serializer = AdminOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
