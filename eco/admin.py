from django.contrib import admin

from .models import *
admin.site.register(UserProfile)
admin.site.register(Order)

admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Wishlist)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)} # new

admin.site.register(Item, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)} # new

admin.site.register(Category, CategoryAdmin)