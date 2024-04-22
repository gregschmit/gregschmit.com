from django.http import HttpResponse
from django.shortcuts import render

# This allows easy DoS, so keep disabled most of the time.
STRESS_TEST = False


def home(request):
    return render(request, "frontend/home.html")


def up(request):
    return HttpResponse("OK")


def stress(request):
    if not STRESS_TEST:
        return HttpResponse("Stress endpoint is disabled.")

    # Do some CPU-bound work.
    n = int(request.GET.get("n", 123456789))
    v = 1
    for _ in range(n):
        v = (v + n) % 1000000
    return HttpResponse(f"Stressed at n = {n}, calculated value is {v}.")
