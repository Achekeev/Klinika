from rest_framework import serializers
from .models import Works, Blogs, Feedback


class WorksCreateSerializer(serializers.ModelSerializer):
    """ Общий список работы """
    class Meta:
        model = Works
        fields = ('opera', 'beforeopera', 'afteropera', 'name')


class BlogsCreateSerializer(serializers.ModelSerializer):
    """ Общий список блоги """
    class Meta:
        model = Blogs
        fields = ('photo', 'name_blog', 'blog', 'url_blog')


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """ Общий список отзывов """
    class Meta:
        model = Feedback
        fields = ('name', 'photo', 'feedback')

