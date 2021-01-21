from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from .models import User
from django.contrib.auth import get_user_model


class CreateUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('pk', 'phone', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone'], password=validated_data['password'],
                                        name=validated_data['name'])
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'phone', 'name', 'balance', 'avatar', 'total_kills')


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)
            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and
    password reset(No login required but otp required)
    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview


class UserPhoneChangeSerializer(ModelSerializer):
    """Изменение телефона"""
    phone = serializers.CharField(required=False, initial="current phone")
    avatar = serializers.ImageField(use_url=True, required=False)


    class Meta:
        model = User
        fields = ['phone', 'name', 'avatar']

    def validate_name(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(name=value).exists():
            raise serializers.ValidationError({"name": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.name = validated_data.get('name', instance.name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        print('instance of phone', instance.phone)
        return instance


class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)