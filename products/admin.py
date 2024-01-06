from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Slider,
    Brand,
    Color,
    Tag,
    Maincategory,
    Category,
    Subcategory,
    Product,
    ProductInformation,
    ProductImage,
    AvailableSize,
    Offer,
    OfferProduct,
    Review,
)


# Register your models here.
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"

admin.site.register(Brand)
admin.site.register(Color)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "background_color")
    search_fields = ("title",)

admin.site.register(Maincategory)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "status")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("status",)
    search_fields = ("name",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('custom_str',)  # Display the custom representation in the admin panel

    def custom_str(self, obj):
        return str(obj)  # Use your __str__ method logic here

    custom_str.short_description = 'Custom Display' 

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1


class ProductInformationInline(admin.TabularInline):
    model = ProductInformation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "subcategory", 'is_active')
    exclude = ("creator",)
    list_filter = (
        "subcategory",
        "is_best_seller",
        "is_offer",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "subcategory__name")  # Add subcategory field for search
    # autocomplete_fields = ("subcategory", "tag")
    inlines = [ProductImageInline, AvailableSizeInline, ProductInformationInline]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    def discount_price(self, obj):
        return obj.get_discount_price()

    image_preview.short_description = "Image Preview"
    discount_price.short_description = "Sale Price"
    
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "weight",
        "unit",
        "discount_price",
        "regular_price",
        "is_stock",
    )
    list_filter = ("product", "unit", "is_stock")

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "offer")

@admin.register(OfferProduct)
class OfferProductAdmin(admin.ModelAdmin):
    list_display = ["offer", "product"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "headline", "approval", "created_at"]
    list_filter = ["approval", "created_at"]
    search_fields = ["headline", "content", "user__username", "product__title"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"