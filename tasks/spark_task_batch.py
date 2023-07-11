from pyspark.sql import SparkSession
import uuid, os
import tasks.helpers_tasks as ht

STORAGE_ACCOUNT='spotpricingstoragedev'
KEY_VAULT_URI='https://spot-pricing-kv-dev.vault.azure.net/'
    
def get_azure_spark_connection(): 
    
    app_id = os.getenv('APP_ID')
    tenant_id = os.getenv('TENANT_ID')
    app_secret = os.getenv('APP_SECRET')
    
    accnt_key = \
        ht\
        .get_key_vault_secret(app_id, 
                              tenant_id, 
                              app_secret, 
                              KEY_VAULT_URI,
                              f"{STORAGE_ACCOUNT}-account-key")
    
    spark = \
        SparkSession\
        .builder\
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-azure:3.3.5')\
        .appName("SpotPricingSpark")\
        .getOrCreate()
        
    spark.sparkContext\
        ._jsc\
        .hadoopConfiguration()\
        .set(f"fs.azure.account.key.{STORAGE_ACCOUNT}.dfs.core.windows.net", 
             accnt_key)

    return spark

class Task:
    def __init__(self, data, output_file:str=None):
        self.data = data
        self.output_file = output_file
    
    def run(self):
        spark = \
            get_azure_spark_connection()
        
        df = \
        spark\
            .read\
            .format("csv")\
            .option("inferSchema", "true")\
            .option("header", "true")\
            .option("sep", "\t")\
            .csv(self.data)
            
        df.show(100)
            
        df = df.limit(1000).toPandas()
        print(df)
        
        df.to_csv(self.output_file, sep="\t", header=True, 
                  index=False)
    

def create_tasks(): 
    new_task = Task(f"abfss://cosmosdata@{STORAGE_ACCOUNT}.dfs.core.windows.net/StaticFiles/regionmapping.tsv", f"output.tsv")
    all_tasks = [new_task]
    
    return all_tasks
