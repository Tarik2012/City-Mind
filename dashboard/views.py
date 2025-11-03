from django.shortcuts import render

def home(request):
    return render(request, "dashboard/home.html")

def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

def predict_view(request):
    return render(request, "dashboard/predict.html")

def about_view(request):
    return render(request, "dashboard/about.html")
