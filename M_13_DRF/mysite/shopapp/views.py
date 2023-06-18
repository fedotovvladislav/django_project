from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .forms import ProductForm
from .models import Product, Order, ProductImage
from .serializers import OrderSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @extend_schema(
        summary="Get one product details by ID",
        description="Retrieve one **product** details, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, **Product** by id not found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Get product list",
        description="Retrieve list of **product**. Returns 404 if not found",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Post new product")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Put method for product by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="Patch product by ID")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="Delete product by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        "id",
        'delivery_address',
        'promocode',
        'user',
        'products',
    ]
    ordering_fields = [
        'id',
        'user',
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
