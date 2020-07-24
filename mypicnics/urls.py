# from django.contrib import admin
from django.urls import path
from .views import PicnicCreateView, PicnicDetailView, ArtworkCreateView, ArtworkDetailView, \
    CritiqueCreateView, PicnicUpdateView, ArtDelete, CritiqueDelete, ArtworkUpdateView, CritiqueUpdateView, NotifCreateView
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home, name='picnic-home'),
    path('notifications/', views.notifications, name='notifications'),
    path('my-picnics/', views.myPicnics, name='my-picnics'),
    path('picnic/new/', PicnicCreateView.as_view(), name='picnic-create'),
    path('picnic/<int:pk>/', PicnicDetailView.as_view(), name='picnic-detail'),
    path('picnic/<int:pk>/update', PicnicUpdateView.as_view(), name='picnic-update'),
    path('picnic/<int:pk>/remove/<int:userid>', views.leavePicnic, name='leavepicnic'),
    path('my-picnics/join', views.joinPicnic, name='join-picnic'),
    path('picnic/<int:pk>/upload/', ArtworkCreateView.as_view(), name='upload'),
    path('picnic/<int:picnicid>/artwork/<int:pk>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('picnic/<int:picnicid>/artwork/<int:pk>/edit', ArtworkUpdateView.as_view(), name='edit-artwork'),
    path('picnic/<int:picnicid>/artwork/<int:pk>/delete', ArtDelete.as_view(), name='artwork-delete'),
    path('picnic/<int:picnicid>/artwork/<int:artworkid>/critique', CritiqueCreateView.as_view(), name='critique'),
    path('picnic/<int:picnicid>/artwork/<int:artworkid>/critique/<int:pk>/delete', CritiqueDelete.as_view(), name='critique-delete'),
    path('picnic/<int:picnicid>/artwork/<int:artworkid>/critique/<int:pk>/edit', CritiqueUpdateView.as_view(), name='edit-critique'),
    path('picnic/<int:picnicid>/artwork/<int:artworkid>/critique/<int:pk>/thank', NotifCreateView.as_view(), name='give-thanks'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
