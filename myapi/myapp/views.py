from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import face_recognition
import base64
import tempfile
from .serializers import ImageBase64Serializer
import os


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        dados = request.data 
        dados['dados'] = 'Dados adicionais'
        serializer = UserSerializer(data=dados)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        path = 'media/' + str(user.image)
        try:
            face_known = face_recognition.load_image_file(path)  # Carrega a imagem
            face_known_encodings = face_recognition.face_encodings(face_known)

            vetor_string = str(face_known_encodings[0])

            vetor_string = vetor_string.replace('[','')
            vetor_string = vetor_string.replace(']','')
            vetor_string = vetor_string.replace('\n','')

            user.dados = vetor_string
            user.save()

        except Exception as e:
            return Response({'error': f"Erro ao processar a imagem: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post','get'])
    def check(self,request):
        
        #Decofiicar a imagem em base64
        if request.method == 'GET':
            return Response({'message': 'Use o método POST para enviar a imagem.'}, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = ImageBase64Serializer(data=request.data)
            if serializer.is_valid():
                dados = serializer.validated_data
                base64_str = str(dados['image'])
                img_data = base64.b64decode(base64_str)
                flag = False
                user_found = None
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(img_data)
                    path = temp_file.name

                try:
                    face_unknown = face_recognition.load_image_file(path)
                    face_unknown_encodings = face_recognition.face_encodings(face_unknown)

                    if not(len(face_unknown_encodings) > 0):
                        return Response({'error': 'Não foi possível identificar o rosto na imagem'}, status=status.HTTP_400_BAD_REQUEST)

                    users = User.objects.all()
                    for user in users:
                        face_know = str(user.dados)
                        face_know = face_know.split()
                        face_know = [float(i) for i in face_know]
                        results = face_recognition.compare_faces([face_know], face_unknown_encodings[0])
                        if results[0]:
                            flag = True
                            user_found = user
                            break

                except Exception as e:
                    return Response({'error': f"Erro ao processar a imagem: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                finally:
                    if os.path.exists(path):  # Garante que o arquivo temporário seja excluído
                        os.remove(path)
                if flag:
                    return Response({'message': f'Usuário {user_found.name} reconhecido'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Usuário não reconhecido'}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
