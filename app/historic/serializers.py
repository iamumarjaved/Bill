import datetime
import decimal
import os

from django.conf.global_settings import MEDIA_URL
from rest_framework import serializers

from core.models import Historic, tblSocInvoicing
from core.mappings import column_mapping
from collections import OrderedDict
from core.models import User
from rest_framework.reverse import reverse


class HistoricSerializer(serializers.ModelSerializer):
    """Serializer for historic model."""
    magazzino_di_carico = serializers.SerializerMethodField()
    lead_time = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    rdduedate_vs_carduedate = serializers.SerializerMethodField()
    rdduedate_vs_required = serializers.SerializerMethodField()
    required_vs_deliv_to_store_599 = serializers.SerializerMethodField()
    invoice_url = serializers.SerializerMethodField()

    def get_invoice_url(self, obj):
        if isinstance(obj, dict):
            invoice = obj.get('invoice')
        else:
            invoice = obj.invoice
        if invoice:
            return os.path.join(MEDIA_URL, 'invoices', f"{invoice}.pdf")
        return None

    class Meta:
        model = Historic
        fields = ["brand","customer_type","customer_code","store_id","store_description","city_code",
                  "country","invoice","logistics_company","ipo_invoice","ipo_company","lgi_invoice",
                  "lgi_company","department_code","cites","pieces","parcels","gross_weight_kg",
                  "volume_m3","shp_status","shp_type_desc","master_shp_n","rd_due_date",
                  "carrier_due_date","booking_user","req_delivery_date","pickup_from_ff_500",
                  "ata_local_ff_platform_530","deliv_to_whs_598","deliv_to_store_599","cs_code",
                  "groupage","sender_cust_desc","sender_country","logistic_no_merch","destination",
                  "execution_date","custom_id","deviation_code","deviation_date",
        "category","responsability","gross_performance","net_performance","other_deviations","comment",
                  "magazzino_di_carico","lead_time","state","rdduedate_vs_carduedate","rdduedate_vs_required",
                  "required_vs_deliv_to_store_599", "invoice_url"]
        read_only_fields = fields
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation_new = OrderedDict()
        for field,value in representation.items():
            try:
                representation_new[column_mapping[field]] = value
            except:
                representation_new[field] = value
        return representation_new

    def get_magazzino_di_carico(self, obj):
        # Check if obj is a dictionary and get the invoice accordingly
        if isinstance(obj, dict):
            invoice = obj.get('invoice')
        else:
            invoice = obj.invoice

        if invoice:
            return "TRECATE" if '-' in invoice else "STABIO"
        return None

    def get_lead_time(self, obj):
        if isinstance(obj, dict):
            start_date = obj.get('pickup_from_ff_500')
            end_date = obj.get('deliv_to_store_599')
        else:
            start_date = obj.pickup_from_ff_500
            end_date = obj.deliv_to_store_599
        if end_date:
            try:
                total_days = (end_date - start_date).days
                # Now exclude weekends between start_date and end_date
                weekdays = [start_date + datetime.timedelta(days=x) for x in range(total_days)]
                working_days = sum(1 for day in weekdays if day.weekday() < 5)
                return working_days
            except:
                return 0
        else:
            return 0

    def get_state(self, obj):
        return "LATE" if self.get_lead_time(obj) > 2 else "ON TIME"

    def _date_difference(self, date1, date2):
        if not date1 or not date2:
            return 0
        else:
            try:
                return (date1 - date2).days
            except:
                date2 = date2.date()
                return (date1 - date2).days

    def _date_difference_check(self, date1, date2):
        return "TRUE" if self._date_difference(date1, date2) == 0 else "FALSE"

    def get_rdduedate_vs_carduedate(self, obj):
        if isinstance(obj, dict):
            return self._date_difference_check(obj.get('rd_due_date'), obj.get('carrier_due_date'))
        return self._date_difference_check(obj.rd_due_date, obj.carrier_due_date)

    def get_rdduedate_vs_required(self, obj):
        if isinstance(obj, dict):
            return self._date_difference_check(obj.get('rd_due_date'), obj.get('req_delivery_date'))
        return self._date_difference_check(obj.rd_due_date, obj.req_delivery_date)

    def get_required_vs_deliv_to_store_599(self, obj):
        if isinstance(obj, dict):
            return self._date_difference_check(obj.get('req_delivery_date'), obj.get('deliv_to_store_599'))
        return self._date_difference_check(obj.req_delivery_date, obj.deliv_to_store_599)


class HistoricListSerializer(serializers.ModelSerializer):
    """Serializer for historic model."""

    class Meta:
        model = Historic
        fields = ["brand","customer_type","customer_code","store_id","store_description","city_code",
                  "country","invoice","logistics_company","ipo_invoice","ipo_company","lgi_invoice",
                  "lgi_company","department_code","cites","pieces","parcels","gross_weight_kg",
                  "volume_m3","shp_status","shp_type_desc","master_shp_n","rd_due_date",
                  "carrier_due_date","booking_user","req_delivery_date","pickup_from_ff_500",
                  "ata_local_ff_platform_530","deliv_to_whs_598","deliv_to_store_599","cs_code",
                  "groupage","sender_cust_desc","sender_country","logistic_no_merch","destination",
                  "retail_handling","domestic_linehaul","sorting","tariff_per_carton","execution_date"]
        read_only_fields = fields

class HistoricSerializerRetailHandling(HistoricListSerializer):
    """Serializer for RetailLinehaul"""
    def get_fields(self):
        fields = super().get_fields()
        fields.pop("domestic_linehaul", None)
        fields.pop("tariff_per_carton", None)
        return fields
    
class HistoricSerializerDomesticLinehaul(HistoricListSerializer):
    """Serializer for RetailLinehaul"""
    def get_fields(self):
        fields = super().get_fields()
        fields.pop("retail_handling", None)
        fields.pop("sorting",None)
        return fields

class HistoricSerializer_giacenze_vs_lgi(HistoricListSerializer):
    """Serializer for giacenze_vs_lgi"""
    rd_due_date_500_diff = serializers.IntegerField()
    mesi_in_giacenza = serializers.IntegerField()
    tariffa_tra_m3_kg = serializers.FloatField()


    def get_rd_due_date_500_diff(self, obj):
        # Handle the data here based on its type or other conditions
        if isinstance(obj['colonna_aggiuntiva'], decimal.Decimal):
            return str(obj['colonna_aggiuntiva'])  # or handle it as you need
        return obj['colonna_aggiuntiva'].isoformat()  # assuming it's a date here

    def get_mesi_in_giacenza(self, obj):
        # Handle the data here based on its type or other conditions
        if isinstance(obj['mesi_in_giacenza'], decimal.Decimal):
            return str(obj['mesi_in_giacenza'])
        return obj['mesi_in_giacenza'].isoformat()

    class Meta:
        model = Historic
        fields = ["brand","customer_type","customer_code","store_id","store_description","city_code",
                    "country","invoice","logistics_company","ipo_invoice","ipo_company","lgi_invoice",
                    "lgi_company","department_code","cites","pieces","parcels","gross_weight_kg",
                    "volume_m3","shp_status","shp_type_desc","master_shp_n","rd_due_date",
                    "carrier_due_date","booking_user","req_delivery_date","pickup_from_ff_500",
                    "ata_local_ff_platform_530","deliv_to_whs_598","deliv_to_store_599","cs_code",
                    "groupage","sender_cust_desc","sender_country","logistic_no_merch","destination",
                    "sorting","tariff_per_carton","execution_date","rd_due_date_500_diff", "mesi_in_giacenza", "tariffa_tra_m3_kg"]
        read_only_fields = fields

class HistoricSerializer_wholesale_distribtion(HistoricListSerializer):
    """Serializer for giacenze_vs_lgi"""
    KG_VS_TAXW = serializers.FloatField()
    magazzino_di_partenza = serializers.CharField()
    societa_fatturazione = serializers.SerializerMethodField()  # Use SerializerMethodField instead of CharField
    whl_distribution = serializers.FloatField()
    remote_destination = serializers.FloatField()
    TARIFFA_CARTONE_CZ = serializers.IntegerField()
    new_customer_code = serializers.IntegerField()
    specific_code = serializers.FloatField()

    def get_societa_fatturazione(self, obj):
        # logic to compute societa_fatturazione based on obj.invoice
        invoice_num = obj.invoice.split('-')[-1] if '-' in obj.invoice else None

        if invoice_num:
            soc_obj = tblSocInvoicing.objects.filter(stealth_in_fattura=invoice_num).first()
            return soc_obj.company if soc_obj else ''
        return ''

    class Meta:
        model = Historic
        fields = ["brand","customer_type","customer_code","store_id","store_description","city_code",
                    "country","invoice","logistics_company","ipo_invoice","ipo_company","lgi_invoice",
                    "lgi_company","department_code","cites","pieces","parcels","gross_weight_kg",
                    "volume_m3","shp_status","shp_type_desc","master_shp_n","rd_due_date",
                    "carrier_due_date","booking_user","req_delivery_date","pickup_from_ff_500",
                    "ata_local_ff_platform_530","deliv_to_whs_598","deliv_to_store_599","cs_code",
                    "groupage","sender_cust_desc","sender_country","logistic_no_merch","destination",
                    "sorting","tariff_per_carton","execution_date","KG_VS_TAXW", "magazzino_di_partenza",
                  "societa_fatturazione", "whl_distribution", "remote_destination", "TARIFFA_CARTONE_CZ",
                  "new_customer_code", "specific_code"]
        read_only_fields = fields

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']