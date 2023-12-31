# Generated by Django 4.2.5 on 2023-09-21 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DESTINATION_N',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DownloadRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='RevenueMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_revenues', models.CharField(max_length=29)),
                ('kering_revenues', models.DecimalField(decimal_places=2, max_digits=10)),
                ('note', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Riepilogo',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('week', models.PositiveSmallIntegerField()),
                ('month', models.PositiveSmallIntegerField()),
                ('magazzino_di_carico', models.CharField(default=None, max_length=20, null=True)),
                ('requested_pick_up', models.DateField(default=None, null=True)),
                ('requested_pick_up_time', models.TimeField(default=None, null=True)),
                ('real_arrival', models.DateTimeField(default=None, null=True)),
                ('pick_up', models.DateTimeField(default=None, null=True)),
                ('lgl_warehouse_cut_off', models.TimeField(default=None, null=True)),
                ('departure_type', models.CharField(default=None, max_length=20, null=True)),
                ('country', models.CharField(default=None, max_length=20, null=True)),
                ('plate_nr', models.CharField(default=None, max_length=20, null=True)),
                ('truck_supplier', models.CharField(default=None, max_length=25, null=True)),
                ('truck_type', models.CharField(default=None, max_length=15, null=True)),
                ('reference_dedicato', models.CharField(default=None, max_length=50, null=True)),
                ('max_load', models.PositiveSmallIntegerField(default=None, null=True)),
                ('second_driver', models.BooleanField(default=False)),
                ('arrival_by_sat', models.DateTimeField(default=None, null=True)),
                ('customs_clearance_sat_perfomed_at', models.DateTimeField(default=None, null=True)),
                ('arrival_by_harbour_shipping_pwc', models.DateTimeField(default=None, null=True)),
                ('customs_clearance_hs_pwc_perfomed_at', models.DateTimeField(default=None, null=True)),
                ('arrival_by_mdl', models.DateTimeField(default=None, null=True)),
                ('customs_clearance_mdl_perfomed_at', models.DateTimeField(default=None, null=True)),
                ('arrival_time_date_at_destination', models.DateTimeField(default=None, null=True)),
                ('warehouse_cut_off', models.TimeField(default=None, null=True)),
                ('unloading_date', models.DateField(default=None, null=True)),
                ('keep_in_transit_dashboard_yes_no', models.BooleanField(default=False)),
                ('keep_in_transit_on', models.DateField(default=None, null=True)),
                ('status_available_date', models.DateField(default=None, null=True)),
                ('parcels_qta', models.PositiveSmallIntegerField(default=None, null=True)),
                ('pieces_qta', models.PositiveSmallIntegerField(default=None, null=True)),
                ('m3', models.FloatField(default=None, null=True)),
                ('peso', models.FloatField(default=None, null=True)),
                ('pallet', models.PositiveSmallIntegerField(default=None, null=True)),
                ('packaging', models.PositiveSmallIntegerField(default=None, null=True)),
                ('stand', models.PositiveSmallIntegerField(default=None, null=True)),
                ('pallett_rotti', models.PositiveSmallIntegerField(default=None, null=True)),
                ('due_date', models.DateField(default=None, null=True)),
                ('deviation_reasons', models.CharField(default=None, max_length=50, null=True)),
                ('saturazione', models.FloatField(default=None, null=True)),
                ('ticket', models.CharField(default=None, max_length=20, null=True)),
                ('id_revenues', models.CharField(default=None, max_length=20, null=True)),
                ('revenues', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('revenues_dedicati', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('co_departure', models.CharField(default=None, max_length=20, null=True)),
                ('co_costum', models.CharField(default=None, max_length=20, null=True)),
                ('co_parking', models.CharField(default=None, max_length=20, null=True)),
                ('co_destination', models.CharField(default=None, max_length=20, null=True)),
                ('routing_rule_trecate', models.CharField(default=None, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=2, unique=True)),
                ('retail_handling_cost', models.FloatField(default=0.0)),
                ('domestic_linehaul_cost', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='TARIFFE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(db_index=True, max_length=3)),
                ('H_and_L_vs_LGI', models.DecimalField(decimal_places=3, default=0.0, max_digits=10, verbose_name='H&L-vs-LGI')),
            ],
        ),
        migrations.CreateModel(
            name='TariffPerCaton',
            fields=[
                ('country', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('city', models.CharField(default=None, max_length=50, null=True)),
                ('tariff', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='tblSocInvoicing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default=None, max_length=50, null=True)),
                ('stealth_in_fattura', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WHL_DISTRIBUTION_N',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(db_index=True, max_length=3)),
                ('TARRIF', models.DecimalField(decimal_places=3, default=0.0, max_digits=10, verbose_name='H&L-vs-LGI')),
                ('departure', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WHOLESALE_TARIFFE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(db_index=True, max_length=3)),
                ('H_and_L_vs_LGI', models.DecimalField(decimal_places=3, default=0.0, max_digits=10, verbose_name='H&L-vs-LGI')),
            ],
        ),
        migrations.CreateModel(
            name='RiepilogoColumnAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(choices=[('id', 'id'), ('week', 'week'), ('month', 'month'), ('magazzino_di_carico', 'magazzino di carico'), ('requested_pick_up', 'requested pick up'), ('requested_pick_up_time', 'requested pick up time'), ('real_arrival', 'real arrival'), ('pick_up', 'pick up'), ('lgl_warehouse_cut_off', 'lgl warehouse cut off'), ('departure_type', 'departure type'), ('country', 'country'), ('plate_nr', 'plate nr'), ('truck_supplier', 'truck supplier'), ('truck_type', 'truck type'), ('reference_dedicato', 'reference dedicato'), ('max_load', 'max load'), ('second_driver', 'second driver'), ('arrival_by_sat', 'arrival by sat'), ('customs_clearance_sat_perfomed_at', 'customs clearance sat perfomed at'), ('arrival_by_harbour_shipping_pwc', 'arrival by harbour shipping pwc'), ('customs_clearance_hs_pwc_perfomed_at', 'customs clearance hs pwc perfomed at'), ('arrival_by_mdl', 'arrival by mdl'), ('customs_clearance_mdl_perfomed_at', 'customs clearance mdl perfomed at'), ('arrival_time_date_at_destination', 'arrival time date at destination'), ('warehouse_cut_off', 'warehouse cut off'), ('unloading_date', 'unloading date'), ('keep_in_transit_dashboard_yes_no', 'keep in transit dashboard yes no'), ('keep_in_transit_on', 'keep in transit on'), ('status_available_date', 'status available date'), ('parcels_qta', 'parcels qta'), ('pieces_qta', 'pieces qta'), ('m3', 'm3'), ('peso', 'peso'), ('pallet', 'pallet'), ('packaging', 'packaging'), ('stand', 'stand'), ('pallett_rotti', 'pallett rotti'), ('due_date', 'due date'), ('deviation_reasons', 'deviation reasons'), ('saturazione', 'saturazione'), ('ticket', 'ticket'), ('id_revenues', 'id revenues'), ('revenues', 'revenues'), ('revenues_dedicati', 'revenues dedicati'), ('co_departure', 'co departure'), ('co_costum', 'co costum'), ('co_parking', 'co parking'), ('co_destination', 'co destination'), ('routing_rule_trecate', 'routing rule trecate')], max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='Historic',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=20)),
                ('customer_type', models.CharField(max_length=20)),
                ('customer_code', models.IntegerField()),
                ('store_id', models.IntegerField()),
                ('customer_description', models.CharField(default=None, max_length=50, null=True)),
                ('store_description', models.CharField(default=None, max_length=50, null=True)),
                ('city_code', models.CharField(default=None, max_length=50, null=True)),
                ('country', models.CharField(max_length=3)),
                ('invoice', models.CharField(db_index=True, max_length=20)),
                ('logistics_invoice', models.CharField(default=None, max_length=20, null=True)),
                ('logistics_company', models.CharField(default=None, max_length=20, null=True)),
                ('invoice_date', models.DateField(default=None, null=True)),
                ('ipo_invoice', models.CharField(default=None, max_length=20, null=True)),
                ('ipo_company', models.CharField(default=None, max_length=20, null=True)),
                ('lgi_invoice', models.CharField(default=None, max_length=20, null=True)),
                ('lgi_company', models.CharField(default=None, max_length=20, null=True)),
                ('prebolla_pda', models.CharField(default=None, max_length=60, null=True)),
                ('purchase_order', models.CharField(default=None, max_length=50, null=True)),
                ('department_code', models.CharField(default=None, max_length=50, null=True)),
                ('department_description', models.CharField(default=None, max_length=50, null=True)),
                ('cites', models.CharField(default=None, max_length=20, null=True)),
                ('pieces', models.IntegerField()),
                ('parcels', models.IntegerField()),
                ('gross_weight_kg', models.FloatField()),
                ('volume_m3', models.FloatField()),
                ('shp_status', models.CharField(default=None, max_length=20, null=True)),
                ('shp_type_code', models.PositiveSmallIntegerField(default=None, null=True)),
                ('shp_type_desc', models.CharField(default=None, max_length=50, null=True)),
                ('carrier', models.CharField(default=None, max_length=15, null=True)),
                ('master_shp_n', models.CharField(default=None, max_length=25, null=True)),
                ('shp_n', models.CharField(default=None, max_length=25, null=True)),
                ('dep_apt', models.CharField(default=None, max_length=20, null=True)),
                ('des_apt', models.CharField(default=None, max_length=20, null=True)),
                ('rd_due_date', models.DateField(default=None, null=True)),
                ('carrier_due_date', models.DateField(default=None, null=True)),
                ('status_a', models.DateTimeField(default=None, null=True)),
                ('status_b', models.DateField(default=None, null=True)),
                ('booking_user', models.CharField(default=None, max_length=20, null=True)),
                ('status_c', models.DateField(default=None, null=True)),
                ('req_delivery_date', models.DateField(default=None, null=True)),
                ('changed_status_to_t_110', models.DateField(default=None, null=True)),
                ('pickup_tms_490', models.DateTimeField(default=None, null=True)),
                ('pickup_from_ff_500', models.DateTimeField(db_column='500_pickup_from_ff', default=None, null=True)),
                ('atd_from_ff_hub_501', models.DateTimeField(default=None, null=True)),
                ('eta_loc_ff_platform_508', models.DateTimeField(default=None, null=True)),
                ('ata_local_ff_platform_530', models.DateTimeField(db_column='530_ata_local_ff_platform', default=None, null=True)),
                ('deliv_to_whs_598', models.DateTimeField(db_column='598_deliv_to_whs', default=None, null=True)),
                ('deliv_to_store_599', models.DateTimeField(db_column='599_deliv_to_store', default=None, null=True)),
                ('cs_code', models.IntegerField(default=None, null=True)),
                ('groupage', models.CharField(default=None, max_length=20, null=True)),
                ('sender_cust_code', models.IntegerField(default=None, null=True)),
                ('sender_store_id', models.CharField(default=None, max_length=20, null=True)),
                ('sender_cust_desc', models.CharField(default=None, max_length=50, null=True)),
                ('sender_store_desc', models.CharField(default=None, max_length=60, null=True)),
                ('sender_country', models.CharField(default=None, max_length=3, null=True)),
                ('status_c_to_a', models.CharField(default=None, max_length=12, null=True)),
                ('logistic_no_merch', models.CharField(default=None, max_length=10, null=True)),
                ('service_code', models.CharField(default=None, max_length=10, null=True)),
                ('service_level', models.CharField(default=None, max_length=5, null=True)),
                ('origin_invoice', models.CharField(default=None, max_length=20, null=True)),
                ('outbound_delivery', models.CharField(default=None, max_length=20, null=True)),
                ('destination', models.CharField(default=None, max_length=50, null=True)),
                ('execution_date', models.DateTimeField()),
                ('user', models.CharField(default=None, max_length=10, null=True)),
                ('deviation_code', models.IntegerField(default=None, null=True)),
                ('deviation_date', models.CharField(default=None, max_length=16, null=True)),
                ('category', models.CharField(default=None, max_length=3, null=True)),
                ('responsability', models.CharField(default=None, max_length=15, null=True)),
                ('gross_performance', models.PositiveSmallIntegerField(default=None, null=True)),
                ('net_performance', models.PositiveSmallIntegerField(default=None, null=True)),
                ('other_deviations', models.CharField(default=None, max_length=100, null=True)),
                ('comment', models.CharField(default=None, max_length=50, null=True)),
                ('encode', models.CharField(max_length=32)),
                ('retail_handling_domestic_linehaul', models.BooleanField(default=False)),
                ('retail_handling_domestic_linehaul_DT', models.DateTimeField(default=None, null=True)),
                ('retail_handling', models.FloatField(default=0.0)),
                ('domestic_linehaul', models.FloatField(default=0.0)),
                ('sorting', models.FloatField(default=0.0)),
                ('custom_id', models.CharField(default=None, max_length=20, null=True)),
                ('tariff_per_carton', models.FloatField(default=0.0)),
                ('retail_handling_domestic_linehaul_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
