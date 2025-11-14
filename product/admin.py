from django.contrib import admin

from.models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_preview')
    search_fields = ('name',)

     # To show image preview in the admin list
    def image_preview(self, obj): # image preview shows a small image thumbnail (directly from Cloudinary URL).
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" height="80" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-id',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" height="80" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"



