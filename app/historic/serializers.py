import decimal

from rest_framework import serializers

from core.models import Historic, tblSocInvoicing
from core.mappings import column_mapping
from collections import OrderedDict

class HistoricSerializer(serializers.ModelSerializer):
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
                  "execution_date","custom_id","deviation_code","deviation_date",
        "category","responsability","gross_performance","net_performance","other_deviations","comment",]
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
