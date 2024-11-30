import random
import time
from http import HTTPStatus

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
import logging

logger = logging.getLogger(__name__)


auth_codes = {}


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone_number = request.user.phone_number
        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            return Response({'error': 'Пользователь не найден'},
                            status=HTTPStatus.NOT_FOUND)
        profile_data = {
            'phone_number': user.phone_number,
            'invite_code':  user.invite_code,
            'activated_invite_code': user.activated_invite_code or 'Не активирован'
        }
        return Response(profile_data, status=HTTPStatus.OK)

    def post(self, request):
        phone_number = request.user.phone_number
        invite_code = request.data.get('invite_code')

        if not invite_code:
            return Response({'error': 'Инвайт-код обязателен'},
                            status=HTTPStatus.BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()
        if user.activated_invite_code:
            return Response({'message': 'Инвайт-код уже активирован'},
                            status=HTTPStatus.BAD_REQUEST)

        inviter = User.objects.filter(invite_code=invite_code).first()
        if not inviter:
            return Response({'error': 'Неверный инвайт-код'}, status=HTTPStatus.BAD_REQUEST)

        user.activated_invite_code = invite_code
        user.invited_by = inviter
        user.save()

        return Response({'message': f'Инвайт-код {invite_code} успешно активирован'},
                        status=HTTPStatus.OK)


class RequestPhoneNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Номер телефона обязателен'},
                            status=HTTPStatus.BAD_REQUEST)

        # генерация 4-значного кода
        auth_code = str(random.randint(1000, 9999))
        global auth_codes
        auth_codes[phone_number] = auth_code
        print(f"Сгенерированный код для {phone_number}: {auth_code}")
        logger.info(f"Сгенерирован код для номера {phone_number}: {auth_code}")

        # задержка отправки
        time.sleep(2)
        return Response({'message': f'Код отправлен на {phone_number}'},
                        status=HTTPStatus.OK)


class RequestAuthCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not phone_number or not auth_code:
            return Response({'error': 'Номер телефона и код обязательны'},
                            status=HTTPStatus.BAD_REQUEST)

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
            return Response({'message': f'Пользователь {phone_number} авторизован'},
                            status=HTTPStatus.OK)
        return Response({'error': 'Неверный код'},
                        status=HTTPStatus.BAD_REQUEST)
