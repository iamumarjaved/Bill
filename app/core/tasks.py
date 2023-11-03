"""Setup CRON task"""

from logging import getLogger
from core.utils.ftp import FTP
import zipfile
import pandas as pd
import numpy as np
import hashlib
import json
import os
import datetime
import warnings
import re

from django.conf import settings


from app.celery import app

from core.models import Historic, DownloadRequest, Tariff, TariffPerCaton
from core.mappings import column_mapping,optional

warnings.filterwarnings('ignore', category=RuntimeWarning, module='django.db.models.fields')

logger = getLogger(__name__)

def encode_string(string, length=16):
    bytes_data = string.encode('utf-8')
    blake2b_hash = hashlib.blake2b(bytes_data, digest_size=length)
    encoded_string = blake2b_hash.hexdigest()
    return encoded_string

def lookup(date_pd_series, format = "%Y-%m-%d %H:%M"):
    dates = {}
    for date in date_pd_series.unique():
        try:
            parsed_date = pd.to_datetime(date, format=format)
            if pd.notnull(parsed_date):
                dates[date] = parsed_date
        except (ValueError, TypeError):
            pass
        
    return date_pd_series.map(dates)

@app.task
def download_file_FTP():
    """Downloads file from ftp server"""
    ftp = FTP(os.environ.get('FTP_HOST'), os.environ.get('FTP_USERNAME'), os.environ.get('FTP_PASSWORD'))
    local_path = os.path.join(settings.STATIC_ROOT,'historic')
    logger.info("Downloading")

    ftp.change_path("/historicbook")

    files = [file for file in ftp.list_files() if file not in [".",".."]]

    if(len(files) == 0):
        print("No new files")
        return

    for file in files:
        ftp.download_file(file,local_path)
        ftp.delete_file(file)
        
    print("Extracting")
    with zipfile.ZipFile(os.path.join(local_path,file), mode="r") as archive:
        archive.extractall(local_path)

    # file = "HistoricBook_20230630111056051982.zip"
    csv_file = file.split(".")[0]+".csv"
    filename = os.path.join(local_path,csv_file)
    print(f"reading {datetime.datetime.now()}")
    # filename = os.path.join(local_path,"HistoricBook_20230622110943085791.csv")
    df = pd.read_csv(filename, sep=";", encoding='windows-1252',dtype=str)
    df = df[df["Shp.Type desc."] != "PDA"]
    df['598_deliv.to WHs_'] = lookup(df['598_deliv.to WHs'])
    df['599_deliv.to store_'] = lookup(df['599_deliv.to store'])
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    filtered_df = df[(df['Shp.status'] == 'Delivered') & ((df['598_deliv.to WHs_'] >= yesterday) | (df['599_deliv.to store_'] >= yesterday))]
    df = df[df["Shp.status"]!="Delivered"]
    df = pd.concat([df,filtered_df]).reset_index(drop=True)
    df = df.fillna('')
    # Calculating ID
    id_list = []
    for record_counter in range(len(df)):
        pickup = df["500_Pickup from FF"][record_counter]
        shp = df["Master Shp.N."][record_counter]
        country = df["Country"][record_counter]
        pattern = "\d{4}[.,/,-]\d{2}[.,/,-]\d{2}"
        try:
            match = re.findall(pattern,pickup)
        except:
            print(pickup)
            print(type(pickup))
        if(len(match) == 0):
            id_list.append(None)
            continue
        if(shp[0] == "'"):
            shp = shp[1:]
        date_token = match[0].split("-")
        current_id = date_token[2]+date_token[1]+date_token[0]+shp+country
        if shp == " ":
            id_list.append(None)
            continue
        if "DHL" in shp:
            id_list.append(None)
            continue
        if "UP" in shp:
            id_list.append(None)
            continue
        if(country == "GB"):
            customer_type = df["Customer type"][record_counter]
            if(customer_type == "WHOLESALE"):
                current_id+="W"
            else:
                current_id+="R"
        id_list.append(current_id)
    df["ID"] = id_list

    print(f"encoding {datetime.datetime.now()}")
    df["encode"] = df.apply(lambda x:encode_string(json.dumps(x[optional.values()].to_dict())),axis=1)
    df["Status A=Available date"] = lookup(df["Status A=Available date"])
    df["Status A=Available date"] = df["Status A=Available date"].fillna(" ")
    
    existing_records = Historic.objects.exclude(shp_status='delivered').only('invoice', 'encode')
    existing_records_dict = {record.invoice: record.encode for record in existing_records}
    new_books = []
    modified_books = []
    print(f"comparing {datetime.datetime.now()}")
    for index,record in df.iterrows():
        historic_invoice = record['Invoice #']
        if historic_invoice in existing_records_dict:
            
            if record["encode"] != existing_records_dict[historic_invoice]:
                modified_books.append(record)
        elif record["Shp.status"].lower() != "delivered":
            new_books.append(record)
    print(f"length of modified {len(modified_books)}")
    print(f"length of new {len(new_books)}")
    print(f"saving {datetime.datetime.now()}")
    batch_size = 500
    for i in range(0, len(modified_books), batch_size):
        batch = modified_books[i:i+batch_size]
        update_objects = []
        update_fields = list(optional.keys()) + ['encode']
        for book in batch:
            try:
                existing_book = Historic.objects.get(invoice=book['Invoice #'])
                kwargs = {}
                for column, key in optional.items():
                    value = book.get(key)
                    if isinstance(value, str) and value.strip() == "":
                        kwargs[column] = None
                    else:
                        kwargs[column] = value
                kwargs["encode"] = book["encode"]
                for attr, value in kwargs.items():
                    setattr(existing_book, attr, value)
                update_objects.append(existing_book)
            except Historic.DoesNotExist:
                pass
        # Perform the bulk update
        Historic.objects.bulk_update(
            update_objects,
            fields=update_fields
        )

    
    
    for i in range(0, len(new_books), batch_size):
        batch = new_books[i:i+batch_size]
        new_books_objects = []
        for book in batch:
            kwargs = {}
            for column, key in column_mapping.items():
                value = book.get(key)
                if isinstance(value, str) and value.strip() == "":
                    kwargs[column] = None
                else:
                    kwargs[column] = value
            kwargs["encode"] = book["encode"]
            parcels = book["Parcels"]
            if(parcels == ""):
                parcels = 0
            parcels = float(parcels)
            retail_tariff,status = Tariff.objects.get_or_create(country=book["Country"])
            kwargs["retail_handling"] = max(float(book["Gross weight Kg."]),float(book["Volume m3"])*200) * retail_tariff.retail_handling_cost
            kwargs["domestic_linehaul"] = max(float(book["Gross weight Kg."]),float(book["Volume m3"])*200) * retail_tariff.domestic_linehaul_cost
            kwargs["sorting"] = 1.5*float(parcels)
            try:
                tariff_per_cartoon = TariffPerCaton.objects.get(country=book["Country"])
                if(tariff_per_cartoon.city):
                    if(tariff_per_cartoon.city.lower() in book["Destination"].lower()):
                        kwargs["tariff_per_carton"] = tariff_per_cartoon.tariff*parcels
                else:
                    kwargs["tariff_per_carton"] = tariff_per_cartoon.tariff*parcels
            except TariffPerCaton.DoesNotExist:
                pass
            new_books_objects.append(Historic(**kwargs))
        Historic.objects.bulk_create(new_books_objects)
    print(f"done {datetime.datetime.now()}")
    files = os.listdir(local_path)
    for file in files:
        try:
            os.remove(os.path.join(local_path,file))
        except:
            pass
    

def rename_columns(column_name):
    if(column_name == "store_id"):
        return "Store ID"
    elif(column_name == "invoice"):
        return "Invoice #"
    elif(column_name == "logistics_company"):
        return "Logistics Company"
    elif(column_name == "ipo_invoice"):
        return "IPO Invoice #"
    elif(column_name == "ipo_company"):
        return "IPO Company"
    elif(column_name == "lgi_invoice"):
        return "LGI Invoice #"
    elif(column_name == "lgi_company"):
        return "LGI Company"
    elif(column_name == "gross_weight_kg"):
        return "Gross weight Kg."
    elif(column_name == "shp_status"):
        return "Shp.status"
    elif(column_name == "shp_type_desc"):
        return "Shp.Type desc."
    elif(column_name == "master_shn_n"):
        return "Master Shp.N."
    elif(column_name == "rd_due_date"):
        return "RD Due date"
    elif(column_name == "carrier_due_date"):
        return "Carrier Due date"
    elif(column_name == "req_delivery_date"):
        return "Req. delivery date"
    elif(column_name == "pickup_from_ff_500"):
        return "500_Pickup from FF"
    elif(column_name == "ata_local_ff_platform_530"):
        return "530_ATA Local FF platform"
    elif(column_name == "deliv_to_whs_598"):
        return "598_deliv.to WHs"
    elif(column_name == "deliv_to_store_599"):
        return "599_deliv.to store"
    elif(column_name == "cs_code"):
        return "CS code"
    elif(column_name == "sender_cust_desc"):
        return "Sender cust.desc."
    elif(column_name == "logistic_no_merch"):
        return "Logistic NO Merch"
    modified_name = column_name.replace('_', ' ').capitalize()
    return modified_name

def reformat(date):
    if date == None:
        return ""
    date = date.split("+")[0]
    datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    modified_string = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
    return modified_string

def reformat_date(date):
    if date == None:
        return ""
    datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    modified_string = datetime_obj.strftime('%d.%m.%Y')
    return modified_string
@app.task
def generate_excel_file(queryset,unique_id):
    # Convert the queryset to a pandas DataFrame
    print(f"Creating DataFrame {len(queryset)}")
    df = pd.DataFrame(queryset,dtype=str)
    df = df.rename(columns=rename_columns)
    df.drop(labels=['Retail handling domestic linehaul','Retail handling domestic linehaul dt','Retail handling domestic linehaul user email'],axis=1,inplace=True)
    df['500_Pickup from FF'] = df['500_Pickup from FF'].apply(lambda x:reformat(x))
    df['530_ATA Local FF platform'] = df['530_ATA Local FF platform'].apply(lambda x:reformat(x))
    df['598_deliv.to WHs'] = df['598_deliv.to WHs'].apply(lambda x:reformat(x))
    df['599_deliv.to store'] = df['599_deliv.to store'].apply(lambda x:reformat(x))
    df['Execution date'] = df['Execution date'].apply(lambda x:reformat(x))
    df["RD Due date"] = df["RD Due date"].apply(lambda x : reformat_date(x))
    df["Carrier Due date"] = df["Carrier Due date"].apply(lambda x : reformat_date(x))
    df["Req. delivery date"] = df["Req. delivery date"].apply(lambda x : reformat_date(x))
    print("Writing")
    file_name = f'generated_file_{unique_id}.csv'
    file_path = os.path.join(settings.STATIC_ROOT,'generated', file_name)
    # Write the DataFrame to the Excel file
    print(file_name)
    df.to_csv(file_path,index=False,sep=";")
    print("returning")
    DownloadRequest.objects.create(unique_id=unique_id)
    return {'unique_id': unique_id, 'file_path': file_path}
