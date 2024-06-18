from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import pymongo
from .serializers import UserSerializer
from api.mongodb import get_db_handle  # Supondo que get_db_handle esteja corretamente implementado

class UserView(APIView):
 
    def get(self, request, format=None):
        try:
            users_collection = get_db_handle().users
            users = list(users_collection.find({}))
            return Response(users, status=status.HTTP_200_OK)
        except pymongo.errors.PyMongoError as e:
            logging.error(f"Erro ao buscar usuários: {e}")
            return Response({"error": "Erro ao buscar usuários"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        logging.info("[USER VIEW]: Requisição post recebida.")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            logging.info("[USER VIEW]: Serializer válido.")
            try:
                users_collection = get_db_handle().users
                user_data = serializer.validated_data
                result = users_collection.insert_one(user_data)
                user_data['_id'] = str(result.inserted_id)
                return Response(user_data, status=status.HTTP_201_CREATED)
            except pymongo.errors.PyMongoError as e:
                logging.error(f"Erro ao inserir usuário: {e}")
                return Response({"error": "Erro ao inserir usuário"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logging.error(f'[USER VIEW]: Serializer inválido: [{serializer.errors}]')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
