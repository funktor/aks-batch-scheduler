from tasks import task as mytask
import argparse
import create_task_helper as cth
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-j", "--job_id", help="Job id", type=str)
    parser.add_argument("-a", "--app_id", help="Client app id", type=str)
    parser.add_argument("-t", "--tenant_id", help="Client tenant id", type=str)
    parser.add_argument("-s", "--app_secret", help="Client app secret", type=str)
    parser.add_argument("-u", "--blob_storage_url", help="Blob storage container URL", type=str)
    parser.add_argument("-c", "--blob_storage_container", help="Blob storage container to store tasks", type=str)
    
    args = parser.parse_args()
    
    # import the relevant create_tasks method (as shown on top)
    cth.create_tasks_and_upload(mytask.create_tasks, 
                                args.job_id, 
                                args.app_id, 
                                args.tenant_id,
                                args.app_secret, 
                                args.blob_storage_url, 
                                args.blob_storage_container)