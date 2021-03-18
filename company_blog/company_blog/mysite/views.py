# from re import I
from django.db.models import Q
# from django.http import JsonResponse
from rest_framework import generics, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from .permission import IsIncidentOwner
from rest_framework.decorators import action
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import Incident, Advertisement, AdvertisementImage, Commentary
from .serializers import (IncidentSerializer, ImageSerializer,
                          IncidentCreateSerializer,
                          # IncidentDetailSerializer,
                          AdvertisementSerializer,
                          AdvertisementCreateSerializer,
                          AdvertisementDetailSerializer,
                          IncidentEditSerializer,
                          AdvertisementEditSerializer,
                          AdImageSerializer,
                          CommentaryCreateSerializer)
from .pagination import ListPagination


class IncidentView(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    pagination_class = ListPagination
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('incident_name',  'owner__email')
    search_fields = ('incident_name',  'owner__email')


class IncidentCreate(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentCreateSerializer

    def get_serializer_context(self):
        context = super(IncidentCreate, self).get_serializer_context()
        print('in views', context, self.request.user.pk)
        context.update({'owner': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        print("post func")
        context = self.request.data
        return self.create(request, owner=self.request.user, *args, **kwargs)


class IncidentDetail(generics.RetrieveDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class IncidentEdit(generics.RetrieveUpdateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentEditSerializer
    http_method_names = ['patch']


class AdView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    pagination_class = ListPagination
    lookup_field = 'pk'

    def qet_queryset(self):
        filter = self.request.get_params.get('filter')
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(title__icontains=filter) | Q(body__icontains=filter))

        return queryset


class AdCreate(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        incident = Incident.objects.get(pk=request.data['incident'])
        if incident.owner == self.request.user:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'OK'}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'You do not have permisions'}, status=status.HTTP_400_BAD_REQUEST)


class AdDetail(generics.RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementDetailSerializer


class AdEdit(generics.RetrieveUpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementEditSerializer
    permission_classes = [IsIncidentOwner]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = AdvertisementImage.objects.all()
    serializer_class = ImageSerializer

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = super().get_queryset()
        queryset = queryset.filter(description__icontains=q)
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentaryCreateView(generics.CreateAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentaryCreateSerializer
    permission_classes = [IsAuthenticated]


class IncidentDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'IncidentDetail.html'

    def get(self, request, pk):
        incident = Incident.objects.get(pk=pk)
        commentary = Commentary.objects.filter(incident=pk)
        return Response({'commentary': commentary, 'incident': incident})