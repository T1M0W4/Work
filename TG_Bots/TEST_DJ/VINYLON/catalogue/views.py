from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import VinylRecord, Tag, AudioFile, Artist
from django.db.models import Q



class CatalogueView(ListView):
    model = VinylRecord
    template_name = "catalogue/catalog.html"
    context_object_name = 'vinyls'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        vinyls_list = VinylRecord.objects.all()

        if query:
            print(query)
            vinyls_list = VinylRecord.objects.filter(
                Q(title__icontains=query) | Q(artist__name__icontains=query) | Q(tags__name__icontains=query)
            )
        return vinyls_list

    def get_context_data(self, **kwargs: any) -> dict:
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.annotate(num_records=models.Count("records")).order_by("-num_records")[:10]
        context['vinyls'] = self.get_queryset()
        return context

        