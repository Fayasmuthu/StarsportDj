from django.db.models import Min, Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
# model
from products.models import Category,Subcategory, Offer,Brand
from products.models import Product
from products.models import Slider
from products.models import Tag
# form
from web.forms import ContactForm
from products.forms import ReviewForm
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db.models import Count

class IndexView(TemplateView):
    template_name = "web/index-5.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(status='Published')
        context["subcategories"] = Subcategory.objects.all()
        products = Product.objects.filter(is_active=True)
        context["popular_products"] = products.filter(is_popular=True)
        context["best_seller_products"] = products.filter(is_best_seller=True)
        context["offers"] = Offer.objects.all()
        context["sliders"] = Slider.objects.all()

         # Check for subcategory and filter products accordingly
        subcategory = self.request.GET.get("subcategory")
        if subcategory:
            subcategory_title = get_object_or_404(Subcategory, slug=subcategory)
            products = products.filter(subcategory=subcategory_title)               
            context["products"] = products
           
        return context


class ShopView(ListView):
    model = Product
    template_name = "web/shop.html"
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        products = Product.objects.all()
        search_query = self.request.GET.get("search")
        category = self.request.GET.get("category")
        subcategory = self.request.GET.get("subcategory")
        sort_by = self.request.GET.get("sort_by")
        # price_range = self.request.GET.get("price-range")
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        category_title = None
        subcategory_title = None

        if min_price and max_price:
            products = products.filter( availablesize__discount_price__range=(min_price, max_price))
        if search_query:
            products = products.filter(Q(name__icontains=search_query))
        if category:
            category_title = Category.objects.get(slug=category)
            products = products.filter(category__slug=category_title)
        if subcategory:
            subcategory_title = Subcategory.objects.get(slug=subcategory)
            products = products.filter(subcategory=subcategory_title)
        if sort_by:
            if sort_by == "low_to_high":
                annotated_queryset = products.annotate(
                    min_discount_price=Min("availablesize__discount_price")
                )
                products = annotated_queryset.order_by("min_discount_price")
            elif sort_by == "high_to_low":
                annotated_queryset = products.annotate(
                    min_discount_price=Min("availablesize__discount_price")
                )
                products = annotated_queryset.order_by("-min_discount_price")
            elif sort_by == "rating":
                products = products.order_by("-rating")
            else:
                products = products.order_by("-id")
        # if price_range:
        #     amount = price_range.replace("₹", "")
        #     try:
        #         min_amount, max_amount = map(int, amount.split("-"))
        #         products = products.filter(
        #             availablesize__discount_price__gte=min_amount,
        #             availablesize__discount_price__lte=max_amount,
        #         ).distinct()
        #     except ValueError:
        #         print("ValueError")

        self.category_title = category_title if category_title else None
        self.subcategory_title = subcategory_title if subcategory_title else None
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(status='Published')
        context["subcategories"] = Subcategory.objects.all()
        context["brands"] = Brand.objects.annotate(store_count=Count('title'))
        context["tags"] = Tag.objects.all()
        context["title"] = self.category_title
        context["Sub_title"] = self.subcategory_title
        return context



def filter_data(request):
    selected_brand = request.GET.getlist('brands[]')
    print("Selected Brands:", selected_brand)  # Add this line for debugging

    if selected_brand:
        course = Product.objects.filter(brand__id__in = selected_brand).order_by('-id')
    else:
        course = Product.objects.all().order_by('-id')

    t = render_to_string('ajax/shop.html', {'course': course})
    return JsonResponse({'data': t})

from django.http import JsonResponse

def filter_range_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price range
    products = Product.objects.filter(availablesize__discount_price__range=(min_price, max_price))

    # Render the products as HTML
    html = render_to_string('ajax/rangeprice.html', {'products': products})

    # Return the HTML response
    return JsonResponse({'html': html})

class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.get_object()
        related_products = Product.objects.filter(
            subcategory=current_product.subcategory
        ).exclude(pk=current_product.pk)[:12]
        context["related_products"] = related_products
        context["reviews"] = current_product.reviews.filter(approval=True)
        context["review_form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.get_object()
            user = request.user
            form = ReviewForm(request.POST, request.FILES)

            if form.is_valid():
                form.instance.user = user
                form.instance.product = product
                form.save()
            else:
                print(form.errors)
        return redirect("product:product_detail", slug=self.get_object().slug)


class OfferedProductListView(View):
    template_name = "web/shop.html"

    def get(self, request, offer_id):
        offer = Offer.objects.get(pk=offer_id)
        products = Product.objects.filter(offerproduct__offer=offer)

        context = {
            "offer": offer,
            "offered_products": products,
        }

        return render(request, self.template_name, context)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            "is_contact": True,
            "form": form,
        }
        return render(request, "web/contact.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully Submitted",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)
