from django.shortcuts import render


def home(request):
    context: dict[str, str] = {
        'title': 'Home - Главная',
        'content_1': 'Музыкальная площадка',
        'content_2': 'VINYLON',
    }

    return render(request, 'home/index.html', context)

def about(request):
    context: dict[str, str] = {
        'title': 'Home - О нас',
        'content_1': 'О нас',
        'content_2': 'Интернет магазин виниловых пластинок и музыкальная площадка',
    }

    return render(request, 'home/about.html', context)
