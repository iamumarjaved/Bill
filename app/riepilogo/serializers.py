from rest_framework import serializers
from rest_framework.fields import empty

from core.models import Historic,Riepilogo,RevenueMapper,RiepilogoColumnAccess

class MyModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = (self.context['request'].user)
        editable_fields = []
        if(user and user.groups.exists()):
            editable_fields = RiepilogoColumnAccess.objects.filter(group__in=user.groups.all()).values_list('column',flat=True)

        # Iterate through each field in the serializer
        for field_name, field in self.fields.items():
            # Check if the field is editable
            editable = field_name in editable_fields

            # Retrieve the field type from the underlying model
            model_field = self.Meta.model._meta.get_field(field_name)
            field_type = model_field.get_internal_type()

            # Format the value as desired
            field_value = representation[field_name]
            formatted_value = {
                "value": field_value,
                "type": field_type,
                "editable": editable
            }

            # Update the representation with the formatted value
            representation[field_name] = formatted_value

        return representation

class RiepilogoSerializerAPI(MyModelSerializer):
    """Serializer for the riepilogo used by script to create new record."""
    real_arrival = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    pick_up = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_sat = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_sat_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_harbour_shipping_pwc = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_hs_pwc_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_mdl = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_mdl_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_time_date_at_destination = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    class Meta:
        model = Riepilogo
        fields = ["id","week","month","magazzino_di_carico","requested_pick_up","requested_pick_up_time","real_arrival","pick_up",
                  "lgl_warehouse_cut_off","departure_type","country","id_route","plate_nr","truck_supplier","truck_type","reference_dedicato",
                  "max_load","second_driver","arrival_by_sat","customs_clearance_sat_perfomed_at","arrival_by_harbour_shipping_pwc",
                  "customs_clearance_hs_pwc_perfomed_at","arrival_by_mdl","customs_clearance_mdl_perfomed_at",
                  "arrival_time_date_at_destination","warehouse_cut_off","unloading_date","keep_in_transit_dashboard_yes_no",
                  "keep_in_transit_on","status_available_date","parcels_qta","pieces_qta","m3","peso","pallet","packaging","stand",
                  "pallett_rotti","due_date","deviation_reasons","saturazione","ticket","id_revenues","revenues",
                  "revenues_dedicati","co_departure","co_costum","co_parking","co_destination","routing_rule_trecate"]
        read_only_fields = ["arrival_by_sat","customs_clearance_sat_perfomed_at",
                           "arrival_by_harbour_shipping_pwc","customs_clearance_hs_pwc_perfomed_at",
                           "arrival_by_mdl","customs_clearance_mdl_perfomed_at",
                           "arrival_time_date_at_destination","warehouse_cut_off",
                           "unloading_date","keep_in_transit_dashboard_yes_no","keep_in_transit_on",
                           "status_available_date","parcels_qta","pieces_qta","m3","peso","pallet",
                           "packaging","stand","pallett_rotti","due_date","deviation_reasons",
                           "saturazione","ticket","id_revenues","revenues",
                           "revenues_dedicati","co_departure","co_costum","co_parking","co_destination",
                           "routing_rule_trecate"]
        
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method in ['POST', 'PATCH']:
            # Exclude the fields for POST or PATCH requests
            for field_name in [
                'real_arrival', 'pick_up', 'arrival_by_sat', 'customs_clearance_sat_perfomed_at',
                'arrival_by_harbour_shipping_pwc', 'customs_clearance_hs_pwc_perfomed_at',
                'arrival_by_mdl', 'customs_clearance_mdl_perfomed_at', 'arrival_time_date_at_destination'
            ]:
                fields.pop(field_name, None)
        return fields

class RiepilogoSerializerPatch(serializers.ModelSerializer):
    """Serializer for the riepilogo for patch requests."""
    real_arrival = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    pick_up = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_sat = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_sat_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_harbour_shipping_pwc = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_hs_pwc_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_by_mdl = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    customs_clearance_mdl_perfomed_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    arrival_time_date_at_destination = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    class Meta:
        model = Riepilogo
        fields = '__all__'
        read_only_fields = [
            "warehouse_cut_off","id","week","month","magazzino_di_carico","requested_pick_up","requested_pick_up_time",
            "lgl_warehouse_cut_off","departure_type","country","plate_nr","truck_supplier",
            "truck_type","reference_dedicato","max_load","second_driver","id_revenues","revenues","revenues_dedicati",
            "co_departure","co_costum","co_parking","co_destination","routing_rule_trecate"
        ]

    def update(self, instance, validated_data):
        read_only_fields = self.Meta.read_only_fields
        for field in read_only_fields:
            if field not in validated_data and field in self.initial_data:
                raise serializers.ValidationError({field: ["This field is read-only."]})
            
        request = self.context.get('request')
        user = request.user if request else None
        if(user and user.groups.exists()):
            column_access = RiepilogoColumnAccess.objects.filter(group__in=user.groups.all()).values_list('column',flat=True)
            for entry_column in validated_data.keys():
                if(entry_column not in column_access):
                    raise serializers.ValidationError({entry_column:["You don't have permission to edit this field"]})

        return super().update(instance, validated_data)
    
class ReipilogoSerializerID(serializers.ModelSerializer):
    """Serializer to get id"""
    id = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = Riepilogo
        fields = ['id']
