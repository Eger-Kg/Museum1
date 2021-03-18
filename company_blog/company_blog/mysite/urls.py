from django.urls import path, include
# from company_blog.company_blog.custom_auth.views import register
from .views import IncidentView, IncidentCreate, IncidentDetail, AdView, AdDetail, AdCreate, IncidentEdit, AdEdit,\
    ImageViewSet, CommentaryCreateView, IncidentDetailView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('image', ImageViewSet)

urlpatterns = [
    path('list/', IncidentView.as_view(), name='incident_list'),
    path('create/', IncidentCreate.as_view(), name='incident_create'),
    path('detail/<int:pk>/', IncidentDetail.as_view(), name='incident_detail'),
    path('edit/<int:pk>', IncidentEdit.as_view(), name='incident_edit'),
    path('commentary/create', CommentaryCreateView.as_view(), name='commentary_create'),
    path('incident/<int:pk>', IncidentDetailView.as_view(), name='incident_detail'),
    # Company Advertisement end points
    path('ad/list/', AdView.as_view(), name='ad_list'),
    path('ad/create/', AdCreate.as_view(), name='ad_create'),
    path('ad/<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('ad/edit/<int:pk>', AdEdit.as_view(), name='ad_edit'),
    # image router
    path('', include(router.urls)),

]