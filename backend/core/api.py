from rest_framework.viewsets import ModelViewSet
from core.models import SiteInfo
from core.serializers import SiteInfoSerializer

class SiteInfoViewSet(ModelViewSet):
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer