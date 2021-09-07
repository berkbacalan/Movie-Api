from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from movie.api.pagination import CustomPagination, SmallPagination, LargePagination
from movie.api.permissions import IsAdminUserOrReadOnly
from movie.api.serializers import MovieSerializer, CategorySerializer, SubCategorySerializer
from movie.models import Movie, Category, Subcategory


class MovieListCreateAPIView(ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = CustomPagination
    renderer_classes = [BrowsableAPIRenderer]

    def get_queryset(self):
        queryset = Movie.objects.all()
        movie_name = self.request.query_params.get('movie', None)
        if movie_name is not None:
            queryset = Movie.objects.filter(name=movie_name)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)


@permission_classes([IsAdminUserOrReadOnly])
@renderer_classes([JSONRenderer])
@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@renderer_classes([JSONRenderer])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminUserOrReadOnly, ))
def category_detail_api_view(request, pk):
    try:
        category_instance = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieConcreteAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LargePagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'director', 'category']
    renderer_classes = [BrowsableAPIRenderer]


class MovieDetailConcreteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    renderer_classes = [BrowsableAPIRenderer]


class SubcategoryCreateAPIView(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        category_pk = self.kwargs.get('category_pk')
        category = get_object_or_404(Category, pk=category_pk)
        serializer.save(category=category)


class SubcategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SmallPagination
    renderer_classes = [JSONRenderer]


@renderer_classes([JSONRenderer])
@api_view(['GET'])
def movie_count_api_view(request):
    if request.method == 'GET':
        movie_count = Movie.objects.all().count()
        content = {'movie_count': movie_count}
        return Response(content, status=status.HTTP_200_OK)


@renderer_classes([JSONRenderer])
@api_view(['GET'])
def category_count_api_view(request):
    if request.method == 'GET':
        category_count = Category.objects.all().count()
        content = {'category_count': category_count}
        return Response(content, status=status.HTTP_200_OK)


@renderer_classes([JSONRenderer])
@api_view(['GET'])
def subcategory_count_api_view(request):
    if request.method == 'GET':
        subcategory_count = Subcategory.objects.all().count()
        content = {'subcategory_count': subcategory_count}
        return Response(content, status=status.HTTP_200_OK)


@renderer_classes([JSONRenderer])
@api_view(['GET'])
def category_subcategory_count_apiview(request):
    if request.method == 'GET':
        context = {}
        categories = Category.objects.all()
        for category in categories.iterator():
            subcategories_count = Subcategory.objects.filter(
                parent_category=category).count()
            context.update({str(category): subcategories_count})
        return Response(context, status=status.HTTP_200_OK)


@permission_classes([IsAdminUserOrReadOnly])
@renderer_classes([JSONRenderer])
@api_view(['GET'])
def categories_of_movie_apiview(request, pk):
    if request.method == 'GET':
        context = {}
        ctx = []
        movie = Movie.objects.filter(id=pk).values('name')
        categories_ids = Movie.objects.filter(id=pk).values('category')
        for id in categories_ids.iterator():
            category = Category.objects.filter(
                id=id['category']).values('name')
            print("-->", category)
            ctx.append(category[0]['name'])
        context.update({movie[0]['name']: ctx})
        return Response(context, status=status.HTTP_200_OK)
