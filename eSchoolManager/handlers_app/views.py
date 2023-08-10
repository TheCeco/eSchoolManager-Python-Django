from django.shortcuts import render


# Create your views here.
def handler_404(request, exception):
    return render(request, '404.html', status=404)


def handler_403(request, exception):
    return render(request, '403.html', status=403)


def handler_500(request, exception):
    return render(request, '500.html', status=500)
