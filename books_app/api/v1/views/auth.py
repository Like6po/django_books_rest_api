from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.models.user import User
from api.v1.services.auth import AuthService


class ConfirmRegisterView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Подтверждение регистрации',
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value='Account activated'),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=200),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value='Link not valid'),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def get(self, request: Request, *args, **kwargs):
        auth = AuthService(request)
        result = auth.confirm()
        return Response(result, status=result["status_code"])


class RecoveryUserView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Запросить восстановление аккаунта',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value='Waiting password'),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=200),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value=["Some validation error"]),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.recovery()
        return Response(result, status=result["status_code"])


class RecoveryUserChangePasswordView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Восстановить аккаунт',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["password"],
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value='Password changed'),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=200),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value="Link not valid"),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request, *args, **kwargs):
        auth = AuthService(request)
        result = auth.recovery_change_password()
        return Response(result, status=result["status_code"])


class RegisterUserView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Зарегистрироваться пользователю',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["first_name", "second_name", "email", "password"],
            properties={
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "second_name": openapi.Schema(type=openapi.TYPE_STRING),
                "patronymic": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),

            }
        ),
        responses={
            "201": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_OBJECT,
                                             properties={
                                                 "id": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "patronymic": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "second_name": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "email": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "password": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
                                             }),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=201),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value=["validation error"]),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.register(role=User.ROLES.USER.value)
        return Response(result, status=result["status_code"])


class RegisterAuthorView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Зарегистрироваться автору',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["first_name", "second_name", "email", "password"],
            properties={
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "second_name": openapi.Schema(type=openapi.TYPE_STRING),
                "patronymic": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING)

            }
        ),
        responses={
            "201": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_OBJECT,
                                             properties={
                                                 "id": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "created_at": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "patronymic": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "second_name": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "email": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "password": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                                                 "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
                                             }),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=201),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value=["validation error"]),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.register(role=User.ROLES.AUTHOR.value)
        return Response(result, status=result["status_code"])


class LoginView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Войти',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
                    }),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=200),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value=["validation error"]),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
            "404": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value="User not found"),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=404),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.login()
        return Response(result, status=result["status_code"])


class RefreshView(APIView):
    @swagger_auto_schema(
        tags=['auth'], operation_summary='Обновить токены',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh_token"],
            properties={
                "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING)
                    }),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=200),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Success"),
                }
            ),
            "400": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value=["validation error"]),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=400),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
            "404": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, value="User not found"),
                    'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, value=404),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, value="Failed")
                }
            ),
        }
    )
    def post(self, request: Request):
        auth = AuthService(request)
        result = auth.refresh()
        return Response(result, status=result["status_code"])
