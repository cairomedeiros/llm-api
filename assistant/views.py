from openai import OpenAI
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import OpenAIRequestSerializer
from llmapi.mongodb import get_db_handle

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)

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
