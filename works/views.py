from django.db.models import F
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView

from .serializers import WorksCreateSerializer, BlogsCreateSerializer, FeedbackCreateSerializer

from .models import Works, Blogs, Asks, Feedback


class WorksView(ListCreateAPIView):
    queryset = Works.objects.all()
    serializer_class = WorksCreateSerializer


class BlogsView(ListCreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogsCreateSerializer


class AsksView(APIView):
    def post(self, request):
        name = request.data.get("name")
        phone = request.data.get("phone")
        email = request.data.get("email")
        message = request.data.get("message")
        try:
            user = Asks.objects.create(fio=name, phone=phone, mail=email, message=message)
            return Response(status=201, data={'status': True, 'message': 'Good job'})
        except:
            return Response(status=401, data={'status': True, 'message': 'Can not create this asks'})


class FeedbackView(APIView):

    def get(self, request):
        peremennaya = Feedback.objects.all()
        serializer = FeedbackCreateSerializer(peremennaya, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        photo = request.data.get("photo")
        feedback = request.data.get("feedback")
        try:
            user = Feedback.objects.create(name=name, photo=photo, feedback=feedback)
            return Response(status=201, data={'status': True, 'message': 'Good job'})
        except:
            return Response(status=401, data={'status': True, 'message': 'Can not create this asks'})