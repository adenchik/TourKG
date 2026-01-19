from django.db import models
from django.urls import reverse


class Tour(models.Model):
    """Модель тура"""
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField('Описание')
    short_description = models.CharField('Краткое описание', max_length=300, blank=True)
    image = models.ImageField('Обложка', upload_to='tours/')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    count_max = models.PositiveIntegerField('Макс. кол-во человек', default=10)
    date_start = models.DateTimeField('Дата начала')
    location = models.CharField('Место проведения', max_length=200)
    included = models.TextField('Что включено', blank=True)
    not_included = models.TextField('Что не включено', blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        ordering = ['-date_start']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tours:detail', kwargs={'slug': self.slug})

    @property
    def available_seats(self):
        """Количество доступных мест"""
        booked = self.orders.filter(status='paid').count()
        return max(0, self.count_max - booked)


class TourImage(models.Model):
    """Дополнительные изображения тура"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='tours/gallery/')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение тура'
        verbose_name_plural = 'Изображения туров'
        ordering = ['order']

    def __str__(self):
        return f'Изображение для {self.tour.title}'


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменен'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='orders', verbose_name='Тур')
    customer_name = models.CharField('Имя клиента', max_length=200)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    quantity = models.PositiveIntegerField('Количество билетов', default=1)
    total_price = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.customer_name}'

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.tour.price * self.quantity
        super().save(*args, **kwargs)
