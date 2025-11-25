from django.http import JsonResponse
import traceback

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            print("⛔ ERROR OCCURRED IN BACKEND:")
            traceback.print_exc()

            return JsonResponse(
                {
                    "status": 500,
                    "error": str(e),   # or "Internal Server Error"
                },
                status=500
            )
