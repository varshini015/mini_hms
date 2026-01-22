import requests
from django.http import JsonResponse

def serverless_test(request):
    url = "https://nv9g4iog9h.execute-api.ap-south-1.amazonaws.com/dev/test"
    response = requests.get(url)
    return JsonResponse(response.json())
