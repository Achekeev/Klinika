from django.utils.crypto import get_random_string
from rest_framework import permissions, generics, request, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from xml.etree import ElementTree as ET
from .utils import otp_generator
from .serializers import CreateUserSerializer, ForgetPasswordSerializer, ChangePasswordSerializer, \
    UserDetailsSerializer, LoginUserSerializer, UserPhoneChangeSerializer
from .models import Client, PhoneOTP
from django.db.models import Q
import requests
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None:
            user.first_login = True
            user.save()

        elif user.first_login:
            user.first_login = False
            user.save()

        login(request, user)
        return super().post(request, format=None)


class UserAPI(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserDetailsSerializer

    def get_object(self, ):
        return get_object_or_404(Client, id=self.request.user.id)


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UserProfileChangeAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """Изменение номера телефона, аватар, имя """
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserPhoneChangeSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset = Client.objects.all()


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


def send_sms_otp(phone_number, message):
    message_id = get_random_string(8)
    login = 'mirsoft'
    password = 'L_GjVzf_'

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>\n
        <id>{message_id}</id>
        <sender>riom.kg</sender>
        <text>{message}</text>
        <time></time>
        <phones>
            <phone>{phone_number}</phone>
        </phones>

    </message>'''

    r = requests.post('https://smspro.nikita.kg/api/message', data=xml.encode('UTF-8'),
                      headers={'content-type': 'application/xml; charset=utf-8'})
    print(type(r.content))
    print(r.content)
    resp = ET.fromstring(r.content)
    s_code = resp.find('.//status')
    failed = True
    if s_code == '0':
        message = 'success'
        failed = False
    elif s_code == '4':
        message = 'Пополните баланс Nikita.kg'
    else:
        message = 'Ошибка'
    return message, failed


def send_otp(phone):
    if phone:
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        message = f'Activation code is {otp_key}'
        try:
            send_sms_otp(phone, message)
        except:
            pass
        return (otp_key)
    else:
        return False


def send_otp_forgot(phone):
    if phone:
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        user = get_object_or_404(Client, phone__iexact=phone)
        if user.name:
            name = user.name
        else:
            name = phone

        message = f'Activation code is {otp_key}'

        try:
            send_sms_otp(phone, message)
        except:
            pass
        return otp_key
    else:
        return False


class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = Client.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                # logic to send the otp and store the phone number and that otp in table.
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    print(old.exists())
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    else:
                        count = count + 1
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            count=count
                        )
                    if count > 7:
                        return Response({
                            'status': False,
                            'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })
            return Response({
                'status': True, 'detail': 'Otp has been sent successfully.'
            })
        else:
            return Response({
                'status': 'False', 'detail': "I haven't received any phone number. Please do a POST request."
            })


class ValidateOTP(APIView):
    """
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password

    """

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })
        else:
            return Response({
                'status': 'False',
                'detail': 'Either phone or otp was not received in Post request'
            })


class RegisterView(APIView):
    """Takes phone and a password and creates a new user only if otp was verified and phone is new"""

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        name = request.data.get('name', False)

        if phone and password:
            phone = str(phone)
            user = Client.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password, 'name': name}
                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Congrats, user has been created successfully.'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Phone number not recognised. Kindly request a new otp with this number'
                    })
        else:
            return Response({
                'status': False,
                'detail': 'Either phone or password was not received in Post request'
            })


class ValidatePhoneForgot(APIView):
    """Validate if account is there for a given phone number and then send otp for forgot password reset"""

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = Client.objects.filter(phone__iexact=phone)
            if user.exists():
                otp = send_otp_forgot(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        k = old.count
                        if k > 10:
                            return Response({
                                'status': False,
                                'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        old.count = k + 1
                        old.save()

                        return Response(
                            {'status': True, 'detail': 'OTP has been sent for password reset. Limits about to reach.'})

                    else:
                        count = count + 1

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=otp,
                            count=count,
                            forgot=True,

                        )
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})

                else:
                    return Response({
                        'status': False, 'detail': "OTP sending error. Please try after some time."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number not recognised. Kindly try a new account for this number'
                })


class ForgotValidateOTP(APIView):
    """
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset
     the forgotted password
    """

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                if old.forgot == False:
                    return Response({
                        'status': False,
                        'detail': 'This phone havenot send valid otp for forgot password. Request a new otp or contact help centre.'
                    })

                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to create new password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Phone not recognised. Kindly request a new otp with this number'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Either phone or otp was not recieved in Post request'
            })


class ForgetPasswordChange(APIView):
    """
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password.
     All three should match.APIView
    """

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp = request.data.get("otp", False)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact=phone) & Q(otp__iexact=otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone': phone,
                        'password': password
                    }
                    user_obj = get_object_or_404(Client, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data=post_data)
                    serializer.is_valid(raise_exception=True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Password changed successfully. Please Login'
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                })

        else:
            return Response({

                'status': False,
                'detail': 'Post request have parameters missing.'
            })
