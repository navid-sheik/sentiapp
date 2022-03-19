


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


def test(request):
    test_func.delay()
    return HttpResponse("Done")