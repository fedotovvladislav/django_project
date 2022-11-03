from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('accounts/profile/edit/<int:pk>', views.UpdateProfileView.as_view(), name='edit_profile'),
    path('accounts/profile/view/<int:pk>', views.DetailProfileView.as_view(), name='view_profile'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='detail_view'),
    path('blogs/create/', views.CreateBlogView.as_view(), name='create_blog'),
    path('blogs/upload/', views.UploadBlogFile.as_view(), name='upload_blog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)