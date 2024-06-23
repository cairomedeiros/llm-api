from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from llamaapi import LlamaAPI

from django.conf import settings
from .serializers.user_serializers import UserSerializer
from .serializers.llama_serializers import LlamaSerializer
from llmapi.mongodb import get_db_handle

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)

class UserView(APIView):
    def get(self, request, format=None):
        try:
            collection = get_db_handle().users
            users = list(collection.find({}))
            serializer = UserSerializer(users, many=True)

            logging.info(f"Successfully retrieved {len(users)} users")

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                collection = get_db_handle().users
                result = collection.insert_one(serializer.validated_data)
                new_user = collection.find_one({"_id": result.inserted_id})

                new_user_serializer = UserSerializer(new_user)

                logging.info(f"Successfully created user with id {result.inserted_id}")

                return Response(new_user_serializer.data, status=status.HTTP_201_CREATED)
            else:
                logging.error(f"Serializer inválido: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LlamaView(APIView):
    def post(self, request, format=None):
        serializer = serializer = LlamaSerializer(data=request.data)
        llama = LlamaAPI(settings.LLAMA_KEY)

        if serializer.is_valid():
            response = llama.run(serializer.validated_data)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

