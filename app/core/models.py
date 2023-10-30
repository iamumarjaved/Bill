"""Database Models"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group
)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """Create and return a new seperuser."""
        user = self.create_user(email=email)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', default='static/images/default.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Historic(models.Model):
    """Historic entity"""
    id = models.AutoField(primary_key=True,db_index=True)
    brand = models.CharField(max_length=20)
    customer_type = models.CharField(max_length=20)
    customer_code = models.IntegerField()
    store_id = models.IntegerField()
    customer_description = models.CharField(max_length=50,
                                            default=None,
                                            null=True)

    store_description = models.CharField(max_length=50,
                                         default=None,
                                         null=True)
    city_code = models.CharField(max_length=50,default=None,null=True)
    country = models.CharField(max_length=3)
    invoice = models.CharField(max_length=20,db_index=True)
    logistics_invoice = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    logistics_company = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    invoice_date = models.DateField(null=True,default=None)
    ipo_invoice = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    ipo_company = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    lgi_invoice = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    lgi_company = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    prebolla_pda = models.CharField(max_length=60,
                                    default=None,
                                    null=True)
    purchase_order = models.CharField(max_length=50,
                                      default=None,
                                      null=True)
    department_code = models.CharField(max_length=50,
                                        default=None,
                                       null=True)
    department_description = models.CharField(max_length=50,
                                         default=None,
                                         null=True)
    cites = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    pieces = models.IntegerField()
    parcels = models.IntegerField()
    gross_weight_kg = models.FloatField()
    volume_m3 = models.FloatField()
    shp_status = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    shp_type_code = models.PositiveSmallIntegerField(default=None,null=True)#1-9
    shp_type_desc = models.CharField(max_length=50,
                                         default=None,
                                         null=True)
    carrier = models.CharField(max_length=15,
                               default=None,
                               null=True)
    master_shp_n = models.CharField(max_length=25,
                                         default=None,
                                         null=True)
    shp_n = models.CharField(max_length=25,
                                         default=None,
                                         null=True)
    dep_apt = models.CharField(max_length=20,
                               default=None,
                               null=True)
    des_apt = models.CharField(max_length=20,
                               default=None,
                               null=True)
    rd_due_date = models.DateField(default=None,
                                    null=True)
    carrier_due_date = models.DateField(default=None,
                                    null=True)
    status_a = models.DateTimeField(default=None,
                                    null=True)
    status_b = models.DateField(default=None,
                                null=True)
    booking_user = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    status_c = models.DateField(default=None,
                                null=True)
    req_delivery_date = models.DateField(default=None,
                                    null=True)
    changed_status_to_t_110 = models.DateField(default=None,
                                               null=True)
    pickup_tms_490 = models.DateTimeField(default=None,
                                          null=True)
    pickup_from_ff_500 = models.DateTimeField(db_column='500_pickup_from_ff',default=None,null=True)
    atd_from_ff_hub_501 = models.DateTimeField(default=None,
                                           null=True)
    eta_loc_ff_platform_508 = models.DateTimeField(default=None,
                                               null=True)
    ata_local_ff_platform_530 = models.DateTimeField(db_column='530_ata_local_ff_platform',default=None,null=True)
    deliv_to_whs_598 = models.DateTimeField(db_column='598_deliv_to_whs',default=None,null=True)
    deliv_to_store_599 = models.DateTimeField(db_column='599_deliv_to_store',default=None,null=True)
    cs_code = models.IntegerField(default=None,
                                    null=True)
    groupage = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    sender_cust_code = models.IntegerField(default=None,
                                        null=True)
    sender_store_id = models.CharField(max_length=20,
                                       default=None,
                                       null=True)
    sender_cust_desc = models.CharField(max_length=50,
                                        default=None,
                                        null=True)
    
    sender_store_desc = models.CharField(max_length=60,
                                         default=None,
                                         null=True)
    sender_country = models.CharField(max_length=3,
                                         default=None,
                                         null=True)
    status_c_to_a = models.CharField(max_length=12,
                                     default=None,
                                     null=True)
    logistic_no_merch = models.CharField(max_length=10,
                                         default=None,
                                         null=True)
    service_code = models.CharField(max_length=10,
                                    default=None,
                                    null=True)
    service_level = models.CharField(max_length=5,
                                         default=None,
                                         null=True)
    origin_invoice = models.CharField(max_length=20,
                                      default=None,
                                      null=True)
    outbound_delivery = models.CharField(max_length=20,
                                         default=None,
                                         null=True)
    destination = models.CharField(max_length=50,
                                         default=None,
                                         null=True)
    execution_date = models.DateTimeField()
    user = models.CharField(max_length=10,
                            default=None,
                            null=True)
    deviation_code = models.IntegerField(default=None,
                                         null=True)
    deviation_date = models.CharField(max_length=16,
                                      default=None,
                                      null=True)
    category = models.CharField(max_length=3,
                                default=None,
                                null=True)
    responsability = models.CharField(max_length=15,
                                      default=None,
                                      null=True)
    gross_performance = models.PositiveSmallIntegerField(default=None,
                                                         null=True)
    net_performance = models.PositiveSmallIntegerField(default=None,
                                        null=True)
    other_deviations = models.CharField(max_length=100,
                                        default=None,
                                        null=True)
    comment = models.CharField(max_length=50,
                               default=None,
                                        null=True)
    encode = models.CharField(max_length=32,null=False,blank=False)
    retail_handling_domestic_linehaul = models.BooleanField(default=False)
    retail_handling_domestic_linehaul_DT = models.DateTimeField(default=None,null=True)
    retail_handling_domestic_linehaul_user = models.ForeignKey(
     User,
     on_delete=models.CASCADE,
     default=None,
     null=True   
    )
    retail_handling = models.FloatField(default=0.0)
    domestic_linehaul = models.FloatField(default=0.0)
    sorting = models.FloatField(default=0.0)
    custom_id = models.CharField(max_length=20,default=None,null=True)
    tariff_per_carton = models.FloatField(default=0.0)

class Tariff(models.Model):
    """Model for tarrif"""
    country = models.CharField(max_length=2,unique=True)
    retail_handling_cost = models.FloatField(default=0.0)
    domestic_linehaul_cost = models.FloatField(default=0.0)


class DownloadRequest(models.Model):
    """Model for download request."""
    unique_id = models.CharField(max_length=40)


class Riepilogo(models.Model):
    """Model for Riepilogo Partenze."""
    id = models.CharField(max_length=20,primary_key=True)
    week = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    magazzino_di_carico = models.CharField(max_length=20,default=None,null=True)
    requested_pick_up = models.DateField(default=None,null=True)
    requested_pick_up_time = models.TimeField(default=None,null=True)
    real_arrival = models.DateTimeField(default=None,null=True)
    pick_up = models.DateTimeField(default=None,null=True)
    lgl_warehouse_cut_off = models.TimeField(default=None,null=True)
    departure_type = models.CharField(max_length=20,default=None,null=True)
    country = models.CharField(max_length=20,default=None,null=True)
    plate_nr = models.CharField(max_length=20,default=None,null=True)
    truck_supplier = models.CharField(max_length=25,default=None,null=True)
    truck_type = models.CharField(max_length=15,default=None,null=True)
    reference_dedicato = models.CharField(max_length=50,default=None,null=True)
    max_load = models.PositiveSmallIntegerField(default=None,null=True)
    second_driver = models.BooleanField(default=False)
    arrival_by_sat = models.DateTimeField(default=None,null=True)
    customs_clearance_sat_perfomed_at = models.DateTimeField(default=None,null=True)
    arrival_by_harbour_shipping_pwc = models.DateTimeField(default=None,null=True)
    customs_clearance_hs_pwc_perfomed_at = models.DateTimeField(default=None,null=True)
    arrival_by_mdl = models.DateTimeField(default=None,null=True)
    customs_clearance_mdl_perfomed_at = models.DateTimeField(default=None,null=True)
    arrival_time_date_at_destination = models.DateTimeField(default=None,null=True)
    warehouse_cut_off = models.TimeField(default=None,null=True)
    unloading_date = models.DateField(default=None,null=True)
    keep_in_transit_dashboard_yes_no = models.BooleanField(default=False)
    keep_in_transit_on = models.DateField(default=None,null=True)
    status_available_date = models.DateField(default=None,null=True)
    parcels_qta = models.PositiveSmallIntegerField(default=None,null=True)
    pieces_qta = models.PositiveSmallIntegerField(default=None,null=True)
    m3 = models.FloatField(default=None,null=True)
    peso = models.FloatField(default=None,null=True)
    pallet = models.PositiveSmallIntegerField(default=None,null=True)
    packaging = models.PositiveSmallIntegerField(default=None,null=True)
    stand = models.PositiveSmallIntegerField(default=None,null=True)
    pallett_rotti = models.PositiveSmallIntegerField(default=None,null=True)
    due_date = models.DateField(default=None,null=True)
    deviation_reasons = models.CharField(max_length=50,default=None,null=True)
    saturazione = models.FloatField(default=None,null=True)
    ticket = models.CharField(max_length=20,default=None,null=True)
    # id_concarico = models.CharField(max_length=20,default=None,null=True)
    id_revenues = models.CharField(max_length=20,default=None,null=True)
    revenues = models.DecimalField(null=True,default=None,max_digits=10, decimal_places=2)
    revenues_dedicati = models.DecimalField(null=True,default=None,max_digits=10, decimal_places=2)
    co_departure = models.CharField(max_length=20,null=True,default=None)
    co_costum = models.CharField(max_length=20,null=True,default=None)
    co_parking = models.CharField(max_length=20,null=True,default=None)
    co_destination = models.CharField(max_length=20,null=True,default=None)
    routing_rule_trecate = models.CharField(max_length=15,null=True,default=None)

class RevenueMapper(models.Model):
    """Table for revenue mapping on riepilogo"""
    id_revenues = models.CharField(max_length=29)
    kering_revenues = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=50)

class RiepilogoColumnAccess(models.Model):
    """User Access List for riepilogo view"""
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE)
    column = models.CharField(max_length=100, choices=[(field.name, field.verbose_name) for field in Riepilogo._meta.fields])

class TariffPerCaton(models.Model):
    """Tarrif per carton for historic table"""
    country = models.CharField(max_length=3,primary_key=True)
    city = models.CharField(max_length=50,default=None,null=True)
    tariff = models.FloatField(default=0.0)

class TARIFFE(models.Model):
    """Model for TARIFFE."""
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=3, db_index=True)
    H_and_L_vs_LGI = models.DecimalField(max_digits=10, decimal_places=3, default=0.0, verbose_name="H&L-vs-LGI")

    def __str__(self):
        return self.country

class WHOLESALE_TARIFFE(models.Model):
    """Model for TARIFFE."""
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=3, db_index=True)
    H_and_L_vs_LGI = models.DecimalField(max_digits=10, decimal_places=3, default=0.0, verbose_name="H&L-vs-LGI")

    def __str__(self):
        return self.country

class tblSocInvoicing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=50, default=None, null=True)
    stealth_in_fattura = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return self.company

class DESTINATION_N(models.Model):
    """Model for DESTINATION."""
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50, default=None, null=True)

    class Meta:
        managed = True


class WHL_DISTRIBUTION_N(models.Model):
    """Model for WHL_DISTRIBUTION."""
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=3, db_index=True)
    TARRIF = models.DecimalField(max_digits=10, decimal_places=3, default=0.0, verbose_name="H&L-vs-LGI")
    departure = models.CharField(max_length=50, default=None, null=True)

    class Meta:
        managed = True


class COUNTER(models.Model):
    """Model for COUNTER."""
    counter = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default=None, null=True)

    class Meta:
        managed = True