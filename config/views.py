from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from books.models import BookReview


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class Review_listView(View):
    def get(self, request):
        book_reviews = BookReview.objects.all().order_by('-created_at')
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(book_reviews, page_size)

        page_num = request.GET.get('page', 1)
        page_object = paginator.get_page(page_num)

        return render(request, 'review_list.html', {'page_obj':page_object})