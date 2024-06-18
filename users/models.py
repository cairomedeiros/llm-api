import uuid
from django.db import models
 
 
class UserModel(models.Model):
    id = models.UUIDField('id', primary_key=True, editable=False, default=uuid.uuid4)
    user_name = models.CharField('userName', max_length=25, unique=True)
    data_criacao = models.DateTimeField('dataCriacao', auto_now_add=True)
    data_atualizacao = models.DateTimeField('dataAtualizacao', auto_now=True)
