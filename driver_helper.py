import joblib
import constants
from blob_storage import Blob
import os

def run(path:str, 
        app_id:str, 
        tenant_id:str, 
        app_secret:str, 
        blob_storage_url:str, 
        blob_storage_inp_container:str, 
        blob_storage_op_container:str):
    """
    Run task specified by the input file at path
    
    :param path: Task input file path w/o file name
    :param app_id: Client app id
    :param tenant_id: Client tenant id
    :param app_secret: Client app secret that has access to storage account
    :param blob_storage_url: Blob storage URL
    :param blob_storage_inp_container: Blob storage container for storing task inputs
    :param blob_storage_op_container: Blob storage container for storing task outputs
    """
    blob = Blob(blob_storage_url, app_id, tenant_id, app_secret)
    local_file_path = constants.INPUT_FILE_PATH
    
    print("Reading tasks into local...")
    with open(local_file_path, 'wb') as f:
        f.write(\
            blob.get_blob_stream(\
                blob_storage_inp_container,
                os.path.join(path, constants.INPUT_FILE_PATH) 
            ).readall()
        )
    
    print("Running tasks...")
    new_task = joblib.load(local_file_path)
    new_task.run()
    
    print("Uploading task outputs...")
    blob.upload_file_to_container(\
        local_file_path=\
            new_task.output_file, 
        output_container=blob_storage_op_container, 
        output_file_path=\
            os.path.join(path, new_task.output_file)
    )