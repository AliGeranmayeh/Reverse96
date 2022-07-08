from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('review', views.user_review.as_view(), name="user_review"),
    path('edit_review/<str:pk>', views.edit_user_reviews.as_view(), name="edit_user_review"),
    path('get_user_reviews/<slug:slug>', views.get_user_reviews.as_view(), name="get_user_reviews"),
    path('get_reviews/<str:pk>', views.get_reviews_api.as_view(), name="get_reviews"),
    path('delete_user_reviews/<str:pk>', views.delete_user_reviews.as_view(), name="delete_user_reviews"),
    path('get_location/<str:pk>', views.get_location_api.as_view(), name="get_location_api"),
    path('get_map_locations', views.get_map_location_view.as_view(), name="get_map_location_view"),
    path('get_map_location_reviews', views.get_map_location_view1.as_view(), name="get_map_location_reviews_view"),
    path('get_location_reviews/<str:pk>', views.get_location_reviews.as_view(), name="get_location_reviews_view"),
    path('add_location', views.add_location_api.as_view(), name="add_location_api"),
    #path('comment', views.CommentView.as_view(), name="create-new-comment"),
    #path('poll', views.PollView.as_view(), name="retrieve-poll-objs"),
    path('get_user_comments/<str:pk>', views.CommentViewAPI.as_view(), name="all-comments"),
    path('add_user_comment/<str:pk>', views.SubmitCommentAPI.as_view(), name="add-comment"),
    path('rates/<str:pk>', views.ViewRateView.as_view(), name="all-rates"),
    path('add_user_like/<str:pk>', views.RateView.as_view(), name="add-rate"),
    path('category', views.Category.as_view(), name="limited-area-category"),
    path('search/<slug:pk>',views.SearchView.as_view(),name= "search"),
    path('u_search/<slug:pk>',views.SearchUserView.as_view(),name= "search_user"),
    path('l_search/<slug:pk>',views.SearchLocationView.as_view(),name= "search_location"),

]