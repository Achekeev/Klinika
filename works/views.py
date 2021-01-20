from rest_framework.generics import ListCreateAPIView
from .serializers import WorksCreateSerializer

from .models import Works


class WorksView(ListCreateAPIView):
    queryset = Works.objects.all()
    serializer_class = WorksCreateSerializer
