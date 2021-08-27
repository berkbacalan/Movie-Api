from django.shortcuts import render

# Create your views here.
from movie.models import Movie


def listMovie(request):
    ctx = Movie.objects.all()

    return render(request, 'movie_list.html', {'movies': ctx})
