from django.shortcuts import render
from django.views.generic import ListView
from vinyls.models import VinylRecord, Tag
from orders.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count

class HomePageView(ListView):
    model = VinylRecord
    template_name = 'home/base.html'
    context_object_name = 'vinyls'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отображение топ-10 тегов
        context['top_tags'] = Tag.objects.annotate(num_records=Count('records')).order_by('-num_records')[:10]
        # Отображение заказов для авторизованных пользователей
        if self.request.user.is_authenticated:
            context['orders'] = Order.objects.filter(user=self.request.user)
            
        return context


class SearchResultsView(ListView):
    model = VinylRecord
    template_name = "home/search_results.html"
    context_object_name = "vinyls"

    def get_queryset(self):
        query = self.request.GET.get("query")
        return VinylRecord.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )



# def home(request):
#     context: dict[str, str] = {
#         'title': 'Home - Главная',
#         'content_1': 'Музыкальная площадка',
#         'content_2': 'VINYLON',
#     }

#     return render(request, 'home/index.html', context)

def about(request):
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content_1': 'О нас',
        'content_2': 'Интернет магазин виниловых пластинок и музыкальная площадка',
    }

    return render(request, 'home/about.html', context)
