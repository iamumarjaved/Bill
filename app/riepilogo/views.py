from rest_framework import viewsets,mixins,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from riepilogo.serializers import RiepilogoSerializerAPI,RiepilogoSerializerPatch,ReipilogoSerializerID
from core.models import Riepilogo
from core.pagination import CustomPagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter
class RiepilogoViewSet(viewsets.GenericViewSet,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    """ViewSet for Riepilogo Table"""
    serializer_class = RiepilogoSerializerAPI
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Riepilogo.objects.all().order_by('-requested_pick_up')

    def get_serializer_class(self):
        if(self.action == "partial_update"):
            return RiepilogoSerializerPatch
        elif(self.action == "get_id"):
            return ReipilogoSerializerID
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.queryset, "****************************88888888")
        column_name = self.request.query_params.get('column_name')
        search_query = self.request.query_params.get('search_query')

        if column_name and search_query:
            search_params = {column_name + '__icontains': search_query}
            queryset = queryset.filter(**search_params)

        return queryset
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='column_name',location=OpenApiParameter.QUERY, description='Column Name', required=False, type=str),
            OpenApiParameter(name='search_query',location=OpenApiParameter.QUERY, description='Search Query', required=False, type=str),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='ids',location=OpenApiParameter.QUERY, description='Comma Separated ID\'s', required=False, type=str),
        ]
    )
    def get_id(self,request,*args,**kwargs):
        ids = (self.request.query_params['ids'].split(","))
        data = {
            "id":ids
        }
        serializer = self.get_serializer(data=data)
        if(serializer.is_valid()):
            id_list = serializer.validated_data.get('id', [])
            matching_records = Riepilogo.objects.filter(id__in=id_list)
            matching_ids = matching_records.values('gps_id','id')
            return Response({'matching_ids': matching_ids})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
