from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from .models import Tour, Order
from .forms import OrderForm


class TourListView(ListView):
    """Главная страница со списком туров"""
    model = Tour
    template_name = 'tours/index.html'
    context_object_name = 'tours'

    def get_queryset(self):
        return Tour.objects.filter(is_active=True)


class TourDetailView(DetailView):
    """Детальная страница тура"""
    model = Tour
    template_name = 'tours/detail.html'
    context_object_name = 'tour'

    def get_queryset(self):
        return Tour.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(tour=self.object)
        return context


class OrderCreateView(View):
    """Создание заказа"""

    def post(self, request, slug):
        tour = get_object_or_404(Tour, slug=slug, is_active=True)
        form = OrderForm(request.POST, tour=tour)

        if form.is_valid():
            order = form.save(commit=False)
            order.tour = tour
            order.total_price = tour.price * order.quantity
            order.save()

            messages.success(
                request,
                f'Заказ #{order.id} успешно создан! Мы свяжемся с вами для подтверждения.'
            )
            return redirect('tours:order_success', order_id=order.id)

        messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        return render(request, 'tours/detail.html', {
            'tour': tour,
            'form': form
        })


def order_success(request, order_id):
    """Страница успешного заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'tours/order_success.html', {'order': order})


def offline(request):
    """Оффлайн страница для PWA"""
    return render(request, 'tours/offline.html')
