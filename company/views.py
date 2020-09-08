from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from company.serializer import CompanySerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser


'''class CreateCompanyView (CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    parser_class = (FileUploadParser,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)'''


'''class UpdateCompanyView (UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    parser_class = (FileUploadParser,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(self.request.data)
        return get_object_or_404(Company, user_id=self.request.user.id)'''


class CreateUpdateCompanyView (APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        company = get_object_or_404(Company, user_id=self.request.user.id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        print('NOT valid')
        return Response(status=status.HTTP_400_BAD_REQUEST)


'''class CreateCompanyView (APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    parser_class = (FileUploadParser,)

    @staticmethod
    def post(request):
        data_ = request.data
        user_ = request.user
        data_['user'] = user_.id
        serializer = CompanySerializer(data=data_)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)'''

