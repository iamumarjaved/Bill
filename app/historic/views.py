import os

from django.templatetags.static import static
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter
from historic.serializers import HistoricSerializer,HistoricListSerializer,HistoricSerializerRetailHandling,HistoricSerializerDomesticLinehaul, HistoricSerializer_giacenze_vs_lgi, HistoricSerializer_wholesale_distribtion, CurrentUserSerializer
from core.models import Historic,User, TARIFFE, WHOLESALE_TARIFFE, tblSocInvoicing, WHL_DISTRIBUTION_N, DESTINATION_N, COUNTER, Riepilogo
from core.tasks import generate_excel_file
from core.pagination import CustomPagination
from core.mappings import column_mapping
from django.db.models.functions import Cast, Round, Concat
from django.db.models import DateField, OuterRef, Subquery, DecimalField, Exists, Sum, Window
from django.http import HttpResponse, HttpResponseServerError, FileResponse, Http404, JsonResponse
from django.db.models import Q, F, ExpressionWrapper, DateField,Case, When, Value, CharField
import datetime
import uuid
from django.db.models import IntegerField
from django.db import models
from django.db.models.functions import Cast, TruncDate
# from django.db.models.functions import ExtractMonth, ExtractDay, Ab
from django.db.models import F, Case, When, FloatField
from django.db.models.functions import ExtractMonth, ExtractDay, Abs
from django.db.models import Subquery, OuterRef, Case, When, Value, CharField
from django.db.models.functions import Substr, Right, Length, StrIndex
from django.db.models import Func, Value, CharField
from django.db.models import Sum, Window, F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView

def generate_unique_id():
    return str(uuid.uuid4())

class HistoricViewSet(viewsets.GenericViewSet):
    """View for historic viewsets."""
    serializer_class = HistoricSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Historic.objects.exclude(
        Q(customer_type='WHOLESALE') |
        Q(shp_type_desc='PDA') |
        Q(master_shp_n__contains='DHL') |
        Q(master_shp_n__contains='UP') |
        Q(retail_handling_domestic_linehaul = True) 
    ).filter(
        (Q(ata_local_ff_platform_530__isnull=True) & Q(deliv_to_store_599__isnull=True)) |
        ~Q(ata_local_ff_platform_530=F("deliv_to_store_599"))
    ).select_related('retail_handling_domestic_linehaul_user').annotate(
        retail_handling_domestic_linehaul_user_email=F('retail_handling_domestic_linehaul_user__email')
    ).values(
        "brand", "customer_type", "customer_code", "store_id", "store_description", "city_code",
        "country", "invoice", "logistics_company", "ipo_invoice", "ipo_company", "lgi_invoice",
        "lgi_company", "department_code", "cites", "pieces", "parcels", "gross_weight_kg",
        "volume_m3", "shp_status", "shp_type_desc", "master_shp_n", "rd_due_date",
        "carrier_due_date", "booking_user", "req_delivery_date", "pickup_from_ff_500",
        "ata_local_ff_platform_530", "deliv_to_whs_598", "deliv_to_store_599", "cs_code",
        "groupage", "sender_cust_desc", "sender_country", "logistic_no_merch", "destination",
        "retail_handling_domestic_linehaul", "retail_handling_domestic_linehaul_DT",
        "retail_handling_domestic_linehaul_user_email","retail_handling","domestic_linehaul",
        "sorting", "execution_date","custom_id","tariff_per_carton","deviation_code","deviation_date",
        "category","responsability","gross_performance","net_performance","other_deviations","comment",
    ).order_by('-id')
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['store_description', 'city_code', 'country', 'invoice', 'master_shp_n', 'groupage', 'destination', 'deliv_to_store_599']
    
    def get_serializer_class(self):
        if(self.action == 'list'):
            return HistoricListSerializer
        if(self.action == "retail_handling"):
            return HistoricSerializerRetailHandling
        if(self.action == "domestic_linehaul"):
            return HistoricSerializerDomesticLinehaul
        if(self.action == "giacenze_vs_lgi"):
            return HistoricSerializer_giacenze_vs_lgi
        if (self.action == 'wholesale_distribtion'):
            return HistoricSerializer_wholesale_distribtion

        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if (self.action == 'all'):
            queryset = Historic.objects.all().order_by('-id')
            column_name = self.request.query_params.get('column_name')
            search_query = self.request.query_params.get('search_query')

            if column_name and search_query:
                key = [key for key, val in column_mapping.items() if val == column_name]
                search_params = {key[0] + '__icontains': search_query}
                queryset = queryset.filter(**search_params)


        date_type = self.request.query_params.get('date_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if date_type and start_date and end_date:
            queryset = queryset.filter(Q(**{date_type + "__gte": start_date, date_type + "__lte": end_date}))

        # Filter by region, country, status, brand, customer type, and document type
        for field in ['region', 'country', 'shp_status', 'brand', 'customer_type', 'document_type']:
            value = self.request.query_params.get(field)
            if value and value != '-ALL':
                queryset = queryset.filter(Q(**{field: value}))

        # Return the filtered queryset
        return queryset

    def queryset_to_response(self,queryset):
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        try:
            serializer = serializer_class(queryset, many=True)
            return HttpResponse(serializer.data)
        except Exception as e:
            print(f"Error: {e}")

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date',location=OpenApiParameter.QUERY, description='Start Date', required=False, type=str),
            OpenApiParameter(name='end_date',location=OpenApiParameter.QUERY, description='End Date', required=False, type=str),
            OpenApiParameter(name='column_name',location=OpenApiParameter.QUERY, description='Column Name', required=False, type=str),
            OpenApiParameter(name='search_query',location=OpenApiParameter.QUERY, description='Search Query', required=False, type=str),
        ],
    )
    @action(detail=False, methods=['get'])
    def retail_handling(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

            self.queryset = self.queryset.filter(
                Q(pickup_from_ff_500__gte=start_date) &
                Q(pickup_from_ff_500__lte=end_date)
            )
        counter_obj = COUNTER.objects.get(category='retail_handling')
        counter_obj.counter = self.queryset.count()
        counter_obj.save()
        return self.queryset_to_response(self.queryset)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date',location=OpenApiParameter.QUERY, description='Start Date', required=False, type=str),
            OpenApiParameter(name='end_date',location=OpenApiParameter.QUERY, description='End Date', required=False, type=str),
            OpenApiParameter(name='search',location=OpenApiParameter.QUERY, description='Search', required=False, type=str),
        ],
    )
    @action(detail=False, methods=['get'])
    def domestic_linehaul(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

            self.queryset = self.queryset.filter(
                Q(pickup_from_ff_500__gte=start_date) &
                Q(pickup_from_ff_500__lte=end_date)
            )

        counter_obj = COUNTER.objects.get(category='domestic_linehaul')
        counter_obj.counter = self.queryset.count()
        counter_obj.save()
        return self.queryset_to_response(self.queryset)

    @action(detail=False, methods=['patch'])
    def update_queryset(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        self.queryset.update(
            retail_handling_domestic_linehaul=True,
            retail_handling_domestic_linehaul_DT = datetime.datetime.now(),
            retail_handling_domestic_linehaul_user=user
            )
        return HttpResponse(f"Successfully invoiced")
    
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date',location=OpenApiParameter.QUERY, description='Start Date', required=False, type=str),
            OpenApiParameter(name='end_date',location=OpenApiParameter.QUERY, description='End Date', required=False, type=str),
            OpenApiParameter(name='search',location=OpenApiParameter.QUERY, description='Search', required=False, type=str),
        ],
    )
    @action(detail=False, methods=['get'])
    def all(self,request,*args,**kwargs):
        """Get entire historic book."""
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        self.queryset = self.get_queryset()
        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

            self.queryset = self.get_queryset().filter(
                Q(pickup_from_ff_500__gte=start_date) &
                Q(pickup_from_ff_500__lte=end_date)
            )
        counter_obj = COUNTER.objects.get(category='all')
        counter_obj.counter = self.queryset.count()
        counter_obj.save()
        return self.queryset_to_response(self.queryset)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='invoice_query', location=OpenApiParameter.QUERY, description='Invoice Search Query',
                             required=True, type=str),
        ],
    )
    @action(detail=False, methods=['get'], name='Invoice Search')
    def invoice_search(self, request, *args, **kwargs):
        """
        Search for an invoice based on the provided query.
        """
        invoice_query = self.request.query_params.get('invoice_query', '').strip()

        if not invoice_query:
            return Response({"error": "Invoice query is required."}, status=400)

        self.queryset = self.get_queryset().filter(Q(invoice__icontains=invoice_query))

        return self.queryset_to_response(self.queryset)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='Counter', location=OpenApiParameter.QUERY, description='Total Counter',
                             required=True, type=str),
        ],
    )

    @action(detail=False, methods=['get'], name='Total Counter')
    def total_counter(self, request, *args, **kwargs):
        """Get total counter."""
        gia = COUNTER.objects.get(category='giacenze_vs_lgi')
        wholesale = COUNTER.objects.get(category='wholesale_distribtion')
        all = COUNTER.objects.get(category='all')
        linehaul = COUNTER.objects.get(category='domestic_linehaul')
        retail = COUNTER.objects.get(category='retail_handling')
        repil = Riepilogo.objects.all().count()


        data = {
            "giacenze_vs_lgi": gia.counter,
            "wholesale_distribtion": wholesale.counter,
            "all": all.counter,
            "domestic_linehaul": linehaul.counter,
            "retail_handling": retail.counter,
            "riepilogo": repil
        }

        return JsonResponse(data)

    @extend_schema(
            parameters=[
                OpenApiParameter(name='start_date',location=OpenApiParameter.QUERY, description='Start Date', required=False, type=str),
                OpenApiParameter(name='end_date',location=OpenApiParameter.QUERY, description='End Date', required=False, type=str),
            ],
        )
    @action(detail=False, methods=['get'])
    def download(self, request):
        """Start request for file download."""
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

            self.queryset = self.queryset.filter(
                Q(pickup_from_ff_500__gte=start_date) &
                Q(pickup_from_ff_500__lte=end_date)
            )
        unique_id = generate_unique_id()
        task = generate_excel_file.delay(list(self.queryset),unique_id)
        return HttpResponse(f"Excel file generation has been initiated. Your identifier is {unique_id}")
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', location=OpenApiParameter.QUERY, description='Start Date',
                             required=False, type=str),
            OpenApiParameter(name='end_date', location=OpenApiParameter.QUERY, description='End Date', required=False,
                             type=str),

            OpenApiParameter(name='search', location=OpenApiParameter.QUERY, description='Search', required=False,
                                type=str),
            OpenApiParameter(name='search_query', location=OpenApiParameter.QUERY, description='Search Query',
                             required=False, type=str),

        ],
    )
    @action(detail=False, methods=['get'])
    def giacenze_vs_lgi(self, request, *args, **kwargs):
        try:
            self.queryset = self.get_queryset()


            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date and end_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

                self.queryset = self.queryset.filter(
                    Q(pickup_from_ff_500__gte=start_date) &
                    Q(pickup_from_ff_500__lte=end_date)
                )

            # Filtering based on your criteria
            self.queryset = self.queryset.filter(
                Q(pickup_from_ff_500__isnull = False) &
            Q(shp_status="Delivered") &
            ~Q(shp_type_desc__in=["PDA", "Platform delivery LGI"]),
            ~Q(master_shp_n__startswith="DHL"),
            ~Q(master_shp_n__startswith="UP")
            )

            # Extract date from datetime fields
            self.queryset = self.queryset.annotate(
                deliv_to_store_599_date=Cast('deliv_to_store_599', DateField()),
            )

            # Fetch instances in memory
            model_ids = self.queryset.values_list('id', flat=True)
            instances_to_update = Historic.objects.filter(id__in=model_ids, rd_due_date__isnull=True)

            # Update the instances in memory
            updated_instances = []
            for instance in instances_to_update:
                if instance.ata_local_ff_platform_530:
                    instance.rd_due_date = instance.ata_local_ff_platform_530.date() + datetime.timedelta(days=1)
                else:
                    instance.rd_due_date = instance.deliv_to_store_599
                updated_instances.append(instance)

            # Use bulk_update to save the changes to the database
            Historic.objects.bulk_update(updated_instances, ['rd_due_date'])

            # Calculate the days difference

            self.queryset = self.queryset.annotate(
                days_from_rd_due_date=ExtractDay(F('rd_due_date')),
                days_from_deliv_to_store_599=ExtractDay(F('deliv_to_store_599')),
                months_from_rd_due_date=ExtractMonth(F('rd_due_date')),
                months_from_deliv_to_store_599=ExtractMonth(F('deliv_to_store_599'))
            ).annotate(
                rd_due_date_500_diff=Abs(F('days_from_rd_due_date') - F('days_from_deliv_to_store_599')),
                mesi_in_giacenza=Abs(F('months_from_deliv_to_store_599') - F('months_from_rd_due_date')) + 1
            )

            # Annotate with the greater value
            self.queryset = self.queryset.annotate(
                greater_value_decimal=Cast(
                    Case(
                        When(Q(volume_m3__gt=(F('gross_weight_kg') / 200)), then=F('volume_m3') * 200),
                        default=F('gross_weight_kg')
                    ), DecimalField(max_digits=10, decimal_places=2)
                )
            )

            # Annotate with the "3 Colonna aggiuntiva" value
            tariff_subquery = TARIFFE.objects.filter(country=OuterRef('country')).values('H_and_L_vs_LGI')[:1]
            self.queryset = self.queryset.annotate(
                tariffa_tra_m3_kg=F('greater_value_decimal') * Subquery(tariff_subquery,
                                                                               output_field=DecimalField(max_digits=10,
                                                                                                         decimal_places=2))
            )

            counter_obj = COUNTER.objects.get(category='giacenze_vs_lgi')
            counter_obj.counter = self.queryset.count()
            counter_obj.save()
            return self.queryset_to_response(self.queryset)
        except Exception as e:
            return HttpResponseServerError(str(e))

    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', location=OpenApiParameter.QUERY, description='Start Date',
                             required=False, type=str),
            OpenApiParameter(name='end_date', location=OpenApiParameter.QUERY, description='End Date', required=False,
                             type=str),

            OpenApiParameter(name='search', location=OpenApiParameter.QUERY, description='Search', required=False,
                             type=str),
            OpenApiParameter(name='search_query', location=OpenApiParameter.QUERY, description='Search Query',
                             required=False, type=str),

        ],
    )
    @action(detail=False, methods=['get'])
    def wholesale_distribtion(self, request, *args, **kwargs):
        try:
            self.queryset = self.get_queryset()

            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date and end_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError({'error': 'Invalid date format. Use YYYY-MM-DD.'})

                self.queryset = self.queryset.filter(
                    Q(pickup_from_ff_500__gte=start_date) &
                    Q(pickup_from_ff_500__lte=end_date)
                )


            self.queryset = Historic.objects.all()

            self.queryset = self.queryset.filter(
                Q(customer_type="WHOLESALE") &
                ~Q(shp_type_desc__in=["PDA", "Platform delivery LGI"]) &
                ~Q(master_shp_n__startswith="DHL") &
                ~Q(master_shp_n__startswith="UP")
            )

            # Extract date from datetime fields
            self.queryset = self.queryset.annotate(
                deliv_to_store_599_date=Cast('deliv_to_store_599', DateField()),
            )



            self.queryset = self.queryset.annotate(
                greater_value_decimal=Cast(
                    Case(
                        When(Q(volume_m3__gt=(F('gross_weight_kg') / 200)), then=F('volume_m3') * 200),
                        default=F('gross_weight_kg')
                    ), DecimalField(max_digits=10, decimal_places=2)
                )
            )

            tariff_subquery = WHOLESALE_TARIFFE.objects.filter(country=OuterRef('country')).values('H_and_L_vs_LGI')[:1]
            self.queryset = self.queryset.annotate(
                KG_VS_TAXW=F('greater_value_decimal') * Subquery(tariff_subquery,
                                                                        output_field=DecimalField(max_digits=10,
                                                                                                  decimal_places=2))
            )

            """
            column: magazzino_di_partenza
            """

            self.queryset = self.queryset.annotate(
                magazzino_di_partenza=Case(
                    When(invoice__contains='-', then=Value('TRECATE')),
                    default=Value('STABIO'),
                    output_field=CharField()
                )
            )

            self.queryset = self.queryset.annotate(hyphen_pos=StrIndex(Value('-'), F('invoice')))
            self.queryset = self.queryset.annotate(after_hyphen=Substr(F('invoice'), F('hyphen_pos') + 1))
            self.queryset = self.queryset.annotate(
                hyphen_pos=StrIndex(Value('-'), F('invoice'))
            ).annotate(
                after_hyphen=Substr(F('invoice'), F('hyphen_pos') + 1)
            ).annotate(
                company_name=Subquery(
                    tblSocInvoicing.objects.filter(stealth_in_fattura="some_value")
                    .values('company')[:1]
                )
            )

            """
            column: WHL distribution
            """

            # If the invoice contains '-'
            self.queryset = self.queryset.annotate(
                tarif_value=Subquery(
                    WHL_DISTRIBUTION_N.objects.filter(
                        Q(departure='IT'),
                        Q(country=F('country'))  # Assuming 'country' is the field in your Historic model
                    ).values('TARRIF')[:1]
                )
            )

            # If the invoice does not contain '-'
            self.queryset = self.queryset.annotate(
                tarif_value=Subquery(
                    WHL_DISTRIBUTION_N.objects.filter(
                        Q(departure='CH'),
                        Q(country=F('country'))
                    ).values('TARRIF')[:1]
                )
            )


            # Compute WHL distribution
            self.queryset = self.queryset.annotate(
                whl_distribution=Case(
                    When(invoice__contains="-", then=F('tarif_value') * F('KG_VS_TAXW')),
                    When(~Q(invoice__contains="-"), then=F('tarif_value') * F('KG_VS_TAXW')),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )

            """
            column: Remote destination
            """
            # Annotate the queryset based on the given conditions
            self.queryset = self.queryset.annotate(
                remote_destination=Case(
                    When(
                        Exists(
                            DESTINATION_N.objects.filter(city=OuterRef('destination'))
                        ),
                        then=F('destination') * Value(1.63)
                    ),
                    default=Value(None),
                    output_field=FloatField()
                )
            )


            """
            column: TARIFFA_CARTONE_CZ
            """

            # Annotate formatted_store_id to new_customer_code for all records
            self.queryset = self.queryset.annotate(
                new_customer_code=Case(
                    When(
                        store_id__lt=10,
                        then=Concat(F('customer_code'), Value('0'), F('store_id'))
                    ),
                    default=Concat(F('customer_code'), F('store_id')),
                    output_field=CharField()
                )
            )


            # Annotate parcel_multi for subsequent usage but only for country 'CZ'
            self.queryset = self.queryset.annotate(
                parcel_multi=Case(
                    When(
                        Q(country='CZ'),
                        then=ExpressionWrapper(F('parcels') * Value(15), output_field=IntegerField())
                    ),
                    default=Value(0),
                    output_field=IntegerField()
                )
            )


            # Calculate tariff_value based on conditions but only for country 'CZ'
            tariff_value = Case(
                When(
                    Q(country='CZ') & Q(new_customer_code__in=['64722801', '55742601']),
                    then=F('parcels') * Value(22)
                ),
                When(
                    Q(country='CZ') & Q(parcel_multi__lt=Value(120)),
                    then=Value(120)
                ),
                When(
                    Q(country='CZ'),
                    then=F('parcel_multi')
                ),
                default=Value(0),
                output_field=IntegerField()  # Explicitly set the output field here
            )


            # Now, annotate the queryset with TARIFFA_CARTONE_CZ
            self.queryset = self.queryset.annotate(
                TARIFFA_CARTONE_CZ=tariff_value
            )


            """
            column: Specific code.
            """
            # Create a sub-query to aggregate volume_m3 per day for the specific customer code
            daily_volume = self.queryset.filter(
                new_customer_code='53760202'
            ).annotate(
                daily_volume_sum=Window(
                    expression=Sum('volume_m3'),
                    partition_by=[F('pickup_from_ff_500')]
                )
            )

            # Create final_value for each record in daily_volume
            daily_volume = daily_volume.annotate(
                final_value=ExpressionWrapper(
                    Case(
                        When(
                            daily_volume_sum__gt=0,
                            then=Value(125.0) / F('daily_volume_sum')  # Using 125.0 to ensure it's treated as a float
                        ),
                        default=Value(0.0)  # Using 0.0 to ensure it's treated as a float
                    ),
                    output_field=FloatField()
                )
            )

            # Calculate the specific code by multiplying final_value by volume_m3
            daily_volume = daily_volume.annotate(
                specific_code=F('final_value') * F('volume_m3')
            )

            # Now, integrate this into your main queryset
            self.queryset = self.queryset.annotate(
                specific_code=Case(
                    When(
                        new_customer_code='53760202',
                        then=Subquery(daily_volume.values('specific_code')[:1])
                    ),
                    default=Value(None),
                    output_field=FloatField()
                )
            )

            counter_obj = COUNTER.objects.get(category='wholesale_distribtion')
            counter_obj.counter = self.queryset.count()
            counter_obj.save()
            return self.queryset_to_response(self.queryset)
        except Exception as e:
            return HttpResponseServerError(str(e))


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that user is logged in

    def get(self, request):
        user = request.user
        default_image_url = static('images/default.jpg')
        return Response({
            'email': user.email,
            'name': user.name,
            'profile_image': user.profile_image.url if user.profile_image else default_image_url
        })

def get_invoice(request, invoice_id):
    # Construct file path based on invoice ID
    file_path = f'E:{invoice_id}.pdf'
    if os.path.exists(file_path):
        pdf = open(file_path, 'rb')
        response = FileResponse(pdf, content_type='application/pdf')
        return response
    else:
        return HttpResponse("Invoice not found")