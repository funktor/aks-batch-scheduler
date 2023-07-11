from blob_storage import Blob
import constants as cnt
import joblib, os

def create_tasks_and_upload(create_task_fn, 
                            job_id:str, 
                            app_id:str, 
                            tenant_id:str,
                            app_secret:str, 
                            blob_storage_url:str, 
                            blob_storage_container:str):
    """
    Create tasks and upload tasks as pickle to storage account.
    
    :param create_task_fn: Method to call for creating tasks
    :param job_id: Job id
    :param app_id: Client app id
    :param tenant_id: Client tenant id
    :param app_secret: Client app secret that has access to storage account
    :param blob_storage_url: Blob storage URL
    :param blob_storage_container: Blob storage container for storing tasks
    """
    
    blob = Blob(blob_storage_url, app_id, tenant_id, app_secret)
    
    print("Creating tasks...")
    all_tasks = create_task_fn()
    
    for i in range(len(all_tasks)):
        new_task = all_tasks[i]
        
        folder = os.path.join(job_id, str(i+1))
        pickle_folder = os.path.join("jobs", folder)
        
        if not os.path.exists(pickle_folder):
            os.makedirs(pickle_folder)
        
        pickle_path = os.path.join(pickle_folder, cnt.INPUT_FILE_PATH)
        
        print(f"Pickling into {pickle_path}...")
        joblib.dump(new_task, pickle_path)
        
        upload_path = os.path.join(folder, cnt.INPUT_FILE_PATH)
        
        print(f"Uploading to {upload_path}...")
        blob.upload_file_to_container(\
            pickle_path, 
            blob_storage_container, 
            upload_path
        )
    
    return len(all_tasks)