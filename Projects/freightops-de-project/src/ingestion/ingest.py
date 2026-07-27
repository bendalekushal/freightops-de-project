import boto3
from datetime import date

def ingest_table(table_name, local_path, bucket, ingest_date):
    s3 = boto3.client('s3')
    prefix = f'bronze/{table_name}/ingest_date={ingest_date}/'

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' in response:
        print(f"[SKIP] {table_name}: data already exists at {prefix}")
        return

    key = f'{prefix}{table_name}.csv'
    s3.upload_file(local_path, bucket, key)
    print(f"[UPLOADED] {table_name} -> s3://{bucket}/{key}")

if __name__ == "__main__":
    bucket = 'freightops-data-bendalekushal'
    today = date.today().isoformat()

    tables = [
        'trips', 'loads', 'drivers', 'trucks', 'trailers',
        'customers', 'facilities', 'routes', 'fuel_purchases',
        'maintenance_records', 'safety_incidents', 'delivery_events',
        'driver_monthly_metrics', 'truck_utilization_metrics'
    ]

    for table in tables:
        local_path = f'data/raw/{table}.csv'
        ingest_table(table, local_path, bucket, today)
