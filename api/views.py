from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from openai import OpenAI
from django.conf import settings
from .serializers.user_serializers import UserSerializer
from .serializers.assistant_serializers import OpenAIRequestSerializer
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

class OpenAIAPIView(APIView):
        def post(self, request, format=None):
            serializer = OpenAIRequestSerializer(data=request.data)
            if serializer.is_valid():
                prompt = serializer.validated_data['prompt']

                # Configurar a chave da API do OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY) 
                print(settings.OPENAI_API_KEY)
                    # Fazer a solicitação à API do OpenAI usando a nova interface
                response = client.chat.completions.create(
                     messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="chat",
                  
                )
                result = response['choices'][0]['message']['content'].strip()
                # Salvar a solicitação e resposta no MongoDB
                collection = get_db_handle().openai_requests
                document = {
                    "prompt": prompt,
                    "response": result                    }
                collection.insert_one(document)

                logging.info(f"Successfully processed OpenAI request with prompt: {prompt}")

                return Response({"response": result}, status=status.HTTP_200_OK)
            else:
                logging.error(f"Serializer inválido: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
