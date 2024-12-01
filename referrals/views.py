import logging
import random
import time
from http import HTTPStatus

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import PhoneNumberSerializer, UserProfileSerializer, AuthCodeSerializer, InviteCodeSerializer

logger = logging.getLogger(__name__)


auth_codes = {}


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=HTTPStatus.OK)

    def post(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data['invite_code']

        if request.user.activated_invite_code:
            return Response({'message': 'Инвайт-код уже активирован'}, status=HTTPStatus.BAD_REQUEST)

        inviter = User.objects.filter(invite_code=invite_code).first()
        if not inviter:
            return Response({'error': 'Неверный инвайт-код'}, status=HTTPStatus.BAD_REQUEST)

        request.user.activated_invite_code = invite_code
        request.user.invited_by = inviter
        request.user.save()

        return Response({'message': f'Инвайт-код {invite_code} успешно активирован'}, status=HTTPStatus.OK)



class RequestPhoneNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        # Генерация 4-значного кода
        auth_code = str(random.randint(1000, 9999))
        auth_codes[phone_number] = auth_code

        logger.info(f"Сгенерирован код для {phone_number}: {auth_code}")

        time.sleep(2)  # Задержка для имитации отправки кода
        return Response({'message': f'Код отправлен на {phone_number}'}, status=HTTPStatus.OK)



class RequestAuthCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        auth_code = serializer.validated_data['auth_code']

        save_code = auth_codes.get(phone_number)
        print(f"Сохраненный код для {phone_number}: {save_code}, Полученный код: {auth_code}")
        logger.info(f"Проверка кода для {phone_number}: сохранённый код {save_code}, полученный код {auth_code}")

        if not save_code:
            return Response({'error': 'Код для этого номера телефона не был отправлен'},
                            status=HTTPStatus.BAD_REQUEST)
        if save_code == auth_code:
            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                user = User.objects.create_user(phone_number=phone_number)
                token, _ = Token.objects.get_or_create(user=user)
                print(f"Пользователь: {user}, Токен: {token}")
            return Response({'message': f'Пользователь {phone_number} авторизован'},
                            status=HTTPStatus.OK)
        return Response({'error': 'Неверный код'},
                        status=HTTPStatus.BAD_REQUEST)
