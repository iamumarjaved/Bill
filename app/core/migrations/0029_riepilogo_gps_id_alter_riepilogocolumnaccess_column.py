# Generated by Django 4.2.3 on 2023-09-20 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_riepilogo_co_costum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='riepilogo',
            name='gps_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='riepilogocolumnaccess',
            name='column',
            field=models.CharField(choices=[('id', 'id'), ('gps_id', 'gps id'), ('week', 'week'), ('month', 'month'), ('magazzino_di_carico', 'magazzino di carico'), ('requested_pick_up', 'requested pick up'), ('requested_pick_up_time', 'requested pick up time'), ('real_arrival', 'real arrival'), ('pick_up', 'pick up'), ('lgl_warehouse_cut_off', 'lgl warehouse cut off'), ('departure_type', 'departure type'), ('country', 'country'), ('plate_nr', 'plate nr'), ('truck_supplier', 'truck supplier'), ('truck_type', 'truck type'), ('reference_dedicato', 'reference dedicato'), ('max_load', 'max load'), ('second_driver', 'second driver'), ('arrival_by_sat', 'arrival by sat'), ('customs_clearance_sat_perfomed_at', 'customs clearance sat perfomed at'), ('arrival_by_harbour_shipping_pwc', 'arrival by harbour shipping pwc'), ('customs_clearance_hs_pwc_perfomed_at', 'customs clearance hs pwc perfomed at'), ('arrival_by_mdl', 'arrival by mdl'), ('customs_clearance_mdl_perfomed_at', 'customs clearance mdl perfomed at'), ('arrival_time_date_at_destination', 'arrival time date at destination'), ('warehouse_cut_off', 'warehouse cut off'), ('unloading_date', 'unloading date'), ('keep_in_transit_dashboard_yes_no', 'keep in transit dashboard yes no'), ('keep_in_transit_on', 'keep in transit on'), ('status_available_date', 'status available date'), ('parcels_qta', 'parcels qta'), ('pieces_qta', 'pieces qta'), ('m3', 'm3'), ('peso', 'peso'), ('pallet', 'pallet'), ('packaging', 'packaging'), ('stand', 'stand'), ('pallett_rotti', 'pallett rotti'), ('due_date', 'due date'), ('deviation_reasons', 'deviation reasons'), ('saturazione', 'saturazione'), ('ticket', 'ticket'), ('id_revenues', 'id revenues'), ('revenues', 'revenues'), ('revenues_dedicati', 'revenues dedicati'), ('co_departure', 'co departure'), ('co_costum', 'co costum'), ('co_parking', 'co parking'), ('co_destination', 'co destination'), ('routing_rule_trecate', 'routing rule trecate')], max_length=100),
        ),
    ]
