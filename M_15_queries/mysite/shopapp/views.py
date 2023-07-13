from timeit import default_timer

from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .forms import ProductForm
from .models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer
from .auxiliary_func import user_comparison


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


class LatestProductsFeed(Feed):
    title = "Latest Products"
    description = "Latest Products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description[:200]


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/user-orders-list.html"
    context_object_name = "orders"

    def __init__(self):
        super().__init__()
        self.owner = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context

    def get_queryset(self):
        self.owner = user_comparison(self.request.user, self.kwargs["pk"])
        queryset = Order.objects.filter(user=self.owner).prefetch_related("products").order_by('-created_at')
        return queryset


class UserOrderExportView(View):

    def get(self, request, pk: int=None) -> JsonResponse:
        owner = user_comparison(self.request.user, pk)
        cache_key = "order_data_export"
        data = cache.get(cache_key)
        if data is None:
            orders_data = OrderSerializer(
                Order.objects.filter(user=owner).prefetch_related("products").order_by('id').defer("products__price"),
                many=True,
                context={"request": self.request}
            )
            data = [
                {
                    "pk": order["pk"],
                    "created_at": order["created_at"],
                    "delivery_address": order["delivery_address"],
                    "promocode": order["promocode"],
                    "products": [
                        {
                            "pk": product["pk"],
                            "name": product["name"],
                            "price": product["price"],
                            "discount": product["discount"],
                            "description": product["description"],
                        } for product in order["products"]
                    ]
                }
                for order in orders_data.data
            ]
            cache.set(cache_key, data, 300)

        user_info = {
            "user": {
                "pk": owner.id,
                "username": owner.username,
                "email": owner.email,
            }
        }

        for order in data:
            order.update(user_info)

        return JsonResponse({"orders": data})
