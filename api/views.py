from django.shortcuts import render
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from api.mongodb import get_db_handle  # Supondo que get_db_handle esteja corretamente implementado

class UserView(APIView):
 
    def get(self, request, format=None):
        db_handle, mongo_client = get_db_handle()
        collection = db_handle['users']
        users = list(collection.find({}))

        # Converte ObjectId para string
        for user in users:
            user['_id'] = str(user['_id'])

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    def post(self, request, format=None):
        logging.info("[USER VIEW]: Requisição post recebida.")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            logging.info("[USER VIEW]: Serializer válido.")
            db_handle, mongo_client = get_db_handle()
            collection = db_handle['users']
            user_data = serializer.validated_data
            result = collection.insert_one(user_data)
                   
            user_data['_id'] = str(result.inserted_id)
            return Response(user_data, status=status.HTTP_200_OK)            

        logging.error(f'[USER VIEW]: Serializer inválido: [{serializer.errors}]')
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
