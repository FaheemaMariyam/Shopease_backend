from rest_framework.permissions import IsAdminUser
from product.models import Product
from order.models import Order
from django.contrib.auth import get_user_model #not directly import User from its model bcz,like this it doesnt affect in future if done any changes like model name of user
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count,Sum
from django.db.models.functions import TruncDate
from admin_order.serializer import AdminOrderSerializer

User=get_user_model()

class AdminDashboardView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        total_users=User.objects.filter(is_staff=False,is_superuser=False).count()
        total_products=Product.objects.count()
        total_orders=Order.objects.count()

        #for get the total revenue
        total_revenue_qs=Order.objects.aggregate(total=Sum("total_price"))#it's produce the queryset as dictionary,we only get the value of the key-total
        total_revenue=total_revenue_qs.get("total") or 0 #it get the value corresponding to the key total if nothing its 0

        # Group orders by date and calculate total revenue per date
        revenue_qs = (
            Order.objects
    # Create a new field "date" by extracting only the DATE part from ordered_at (removes time)
            .annotate(date=TruncDate("ordered_at"))
    # Select only "date" so grouping works cleanly
            .values("date")
    # For each date, calculate total revenue for that date
            .annotate(revenue=Sum("total_price"))
    # Sort by date (optional but makes trend graphs correct)
            .order_by("date")
        )

# Convert queryset into a list of dictionaries for JSON response
        revenue_trend = [
            {
        # Convert date to string (ISO format), if date is None return None
                "date": r["date"].isoformat() if r["date"] else None,
        # Convert Decimal → float and ensure no None values
                "revenue": float(r["revenue"] or 0)
            }
            for r in revenue_qs
        ]


        # Query all distinct statuses and count how many orders each has
        status_qs = (
            Order.objects
    # Select only the 'status' field
            .values("status")
    # And annotate it with "value" which is the count of orders for each status
            .annotate(value=Count("id"))
        )

# Convert list of dicts → single dict: {'pending': 5, 'shipped': 3, ...}
# Using lower() to avoid case mismatches
        status_map = {
            s["status"].lower(): s["value"]
            for s in status_qs
        }

# These are the expected statuses to always show in the dashboard
        statuses = ["pending","processing", "shipped", "delivered", "cancelled"]

# Build final list: [{name: "pending", value: 5}, ...]
# If a status doesn't exist in DB, return 0
        status_counts = [
            {"name": s, "value": status_map.get(s, 0)}
            for s in statuses
        ]


        # Get the latest 5 orders with optimized queries
        recent_order_qs = (
            Order.objects
    # Fetch related user in SAME SQL query (avoids extra queries → efficient)
            .select_related("user")
    # Fetch order items and their related products in BULK (avoids N+1 problem)
            .prefetch_related("items__product")
    # Order by newest first
            .order_by("-id")[:5]  # Limit to 5 for dashboard
        )

# Serialize the optimized queryset
        recent_orders = AdminOrderSerializer(
            recent_order_qs,
            many=True
        ).data

        payload={
            "total_users":total_users,
            "total_products":total_products,
            "total_orders":total_orders,
            "total_revenue":float(total_revenue),
            "revenue_trend":revenue_trend,
            "status_counts":status_counts,
            "recent_orders":recent_orders,

        }
        return Response(payload,status=status.HTTP_200_OK)
