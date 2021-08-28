from django.urls import path

from movie.api import views as api_views

urlpatterns = [
    path('movie/', api_views.MovieListCreateAPIView.as_view(), name='movie-list'),
    path('category/', api_views.category_list_create_api_view, name='category-list'),
    path('category/<int:pk>', api_views.category_detail_api_view, name='category-detail'),
    path('movie-concrete/', api_views.MovieConcreteAPIView.as_view(), name='movie-concrete-views'),
    path('movie-concrete/<int:pk>', api_views.MovieDetailConcreteAPIView.as_view(), name='movie-id-concrete-views'),
    path('category/<int:pk>/subcategory-add/', api_views.SubcategoryCreateAPIView.as_view(),
         name='add-subcategory'),
    path('subcategories/<int:pk>', api_views.SubcategoryDetailAPIView.as_view(),
         name='list-subcategory'),
    path('movie/count',api_views.movie_count_api_view,name='count-movie'),
    path('category/count',api_views.category_count_api_view,name='category-count'),
    path('subcategory/count',api_views.subcategory_count_api_view,name='subcategory-count'),
    path('category/subcategory/count',api_views.category_subcategory_count_apiview,name='subcategory-category-count'),
    path('movie/<int:pk>/categories',api_views.categories_of_movie_apiview,name='movie-categories'),
]
