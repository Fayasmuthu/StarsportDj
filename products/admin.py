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
    Available,
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

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}    

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
    list_display = ('name', 'get_maincategory', 'get_category','get_subcategory', 'slug')

    def get_maincategory(self, obj):
        return obj.category.maincategory.title if obj.category and obj.category.maincategory else None
    get_maincategory.short_description = 'Main Category'

    def get_category(self, obj):
        return obj.category.name if obj.category else None
    get_category.short_description = 'Category'

    def get_subcategory(self, obj):
        return obj.subcategory.name if obj.subcategory else None
    get_subcategory.short_description = 'Subategory'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1


class ProductInformationInline(admin.TabularInline):
    model = ProductInformation
    extra = 1

class AvailableInline(admin.TabularInline):
    model = Available
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "get_category", "get_subcategory", 'is_active')
    exclude = ("creator",)
    list_filter = (
        "subcategory__category__maincategory",
        "subcategory__category",
        "subcategory",
        "is_best_seller",
        "is_offer",
        "is_active",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "subcategory__name", "subcategory__category__name", "subcategory__category__maincategory__title")
    inlines = [ProductImageInline, AvailableSizeInline, ProductInformationInline,AvailableInline]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    def get_category(self, obj):
        return obj.subcategory.category.name if obj.subcategory and obj.subcategory.category else None
    get_category.short_description = 'Category'

    def get_subcategory(self, obj):
        return obj.subcategory.name if obj.subcategory else None
    get_subcategory.short_description = 'Subcategory'

    image_preview.short_description = "Image Preview"

class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "weight",
        "unit",
        "sale_price",
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
    list_display = ["fullname","product", "rating", "approval", "created_at"]
    list_filter = ["approval", "created_at"]
    search_fields = ["headline", "content", "user__username", "product__title"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"