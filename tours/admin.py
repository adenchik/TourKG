from django.contrib import admin
from .models import Tour, TourImage, Order


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'date_start', 'count_max', 'is_active']
    list_filter = ['is_active', 'location', 'date_start']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'price']
    date_hierarchy = 'date_start'
    inlines = [TourImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'short_description', 'description', 'image')
        }),
        ('Детали тура', {
            'fields': ('price', 'count_max', 'date_start', 'location')
        }),
        ('Условия', {
            'fields': ('included', 'not_included'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'tour', 'phone', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'tour']
    search_fields = ['customer_name', 'phone', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'phone', 'email')
        }),
        ('Детали заказа', {
            'fields': ('tour', 'quantity', 'total_price', 'status')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
