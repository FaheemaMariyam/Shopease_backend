from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from shopease_user.models import User
from shopease_user.serializer import UserProfileSerializer
from rest_framework.pagination import PageNumberPagination
import math
from django.db.models import Q

class UserPagination(PageNumberPagination):
    page_size = 10  # change as needed
    def get_paginated_response(self, data):
        total_users = self.page.paginator.count
        total_pages = math.ceil(total_users / self.page_size)
        return Response({
            'total_users': total_users,
            'total_pages': total_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination

    def get(self, request):
        # Exclude admins
        users = User.objects.exclude(role="admin").order_by('-date_joined')  # newest first

        # Search by name
        search = request.query_params.get("search")
        if search:
            users = users.filter(Q(name__icontains=search)| Q(id__icontains=search))

        # Pagination
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class AdminDetailView(APIView):
    permission_classes=[IsAdminUser]
    def patch(self,request,pk):
        try:
            user=User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"detail":"user not found"},status=status.HTTP_404_NOT_FOUND)
        if user.role=="admin":
            return Response({"detail": "Admin cannot be blocked"}, status=status.HTTP_400_BAD_REQUEST)
        
        #toggling the block and unblock
        new_status=request.data.get("blocked")
        if new_status is None:
            return Response({"detail":"blocked field required"},status=status.HTTP_400_BAD_REQUEST)
        user.blocked=new_status
        user.save()
        return Response({"message":"status updated","status":new_status},status=status.HTTP_200_OK)
    def delete(self,request,pk):
        try:
            user=User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"detail":"user not found"},status=status.HTTP_404_NOT_FOUND)
        if user.role=="admin":
            return Response({"detail": "Admin cannot be blocked"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"message":"User removed successfully"},status=status.HTTP_200_OK)