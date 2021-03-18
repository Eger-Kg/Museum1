from rest_framework import serializers
from .models import Incident, Advertisement, AdvertisementImage, Commentary


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ('owner', 'incident_name', 'logo', 'date', 'info', 'id')


class IncidentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ('incident_name', 'logo', 'date', 'info')

    def create(self, validated_data):
        print('I STARTED')
        print("create func in ser", self.context)
        owner = self.context.get('owner')
        print('in serializers', self.context)
        incident = Incident.objects.create(owner=owner, **validated_data)
        incident.save()
        return incident


class IncidentDetailSerializer(serializers.ModelSerializer):
    comment = Commentary.objects.all()

    class Meta:
        model = Incident
        fields = ('owner', 'incident_name', 'logo', 'date', 'info', 'id', 'comment')


class IncidentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ('incident_name', 'logo', 'date', 'info')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('incident', 'title', 'body', 'created_at', 'id')

        def to_representation(self, instance):
            representation = super().to_represetation(instance)
            representation['image'] = instance.images.count()
            representation['incident'] = instance.incident.incident_name
            return representation


class AdvertisementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('title', 'body', 'incident')


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('incident', 'title', 'body', 'created_at', 'id')

        def to_representation(self, instance):
            representation = super().to_represetation(instance)
            representation['image'] = ImageSerializer(instance.images.all(), many=True).data
            representation['incident'] = instance.incident.incident_name
            return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ('image', 'description')


class AdvertisementEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('incident', 'title', 'body', 'created_at')


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ('advertisement', 'image')


class CommentaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ('body', 'incident', 'user')

