from django.urls import path

from api.views import BookReviewDetailAPIView, BookReviewAPIView

app_name = 'api'
urlpatterns = [
    path("reviews/", BookReviewAPIView.as_view(), name='review-list'),
    path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name="review-detail"),
]