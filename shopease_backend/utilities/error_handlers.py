from rest_framework.response import Response
from rest_framework import status

def handle_404_error(message="Resource Not Found"):
    return Response(
        {"error": message, "status": 404},
        status=status.HTTP_404_NOT_FOUND
    )

def handle_500_error(message="Internal Server Error"):
    return Response(
        {"error": message, "status": 500},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
