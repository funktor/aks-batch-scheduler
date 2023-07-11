from batch import Batch
import datetime
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-j", "--job_id", help="Job id", type=str)
    parser.add_argument("-k", "--batch_key", help="batch account key", type=str)
    parser.add_argument("-u", "--acr_user", help="acr username", type=str)
    parser.add_argument("-p", "--acr_pwd", help="acr password", type=str)
    parser.add_argument("-s", "--app_secret", help="client app secret", type=str)
    parser.add_argument("-a", "--app_id", help="client app id", type=str)
    parser.add_argument("-t", "--tenant_id", help="client tenant id", type=str)
    parser.add_argument("-f", "--pool_id", help="batch pool id", type=str)
    parser.add_argument("-r", "--batch_url", help="batch account url", type=str)
    parser.add_argument("-v", "--vm_size", help="pool VM type", type=str)
    parser.add_argument("-n", "--pool_count", help="pool node count", type=str)
    parser.add_argument("-i", "--image", help="docker image", type=str)
    parser.add_argument("-l", "--acr_url", help="acr url", type=str)
    parser.add_argument("-m", "--num_tasks", help="number of tasks in job", type=str)
    parser.add_argument("-x", "--blob_storage_url", help="Blob storage container URL", type=str)
    parser.add_argument("-y", "--blob_storage_inp_container", help="Blob storage container to store task inputs", type=str)
    parser.add_argument("-z", "--blob_storage_op_container", help="Blob storage container to store task outputs", type=str)
    
    args = parser.parse_args()
    
    job_id = args.job_id
    pool_id = args.pool_id
        
    batch_obj = Batch(args.batch_url, 
                      args.app_id, 
                      args.tenant_id, 
                      args.app_secret)
    
    try:
        batch_obj.create_pool(pool_id, 
                              args.vm_size, 
                              args.pool_count, 
                              args.image, 
                              args.acr_url, 
                              args.acr_user, 
                              args.acr_pwd)
        
        batch_obj.create_job(job_id, pool_id)
        
        commands = []
        
        for i in range(1, int(args.num_tasks)+1):
            path = f"{job_id}/{i}"
            commands += \
                [f"/bin/bash -c \"source /src/set_env_variables.sh && python /app/driver.py \
                    --path {path} \
                    --app_id {args.app_id} \
                    --tenant_id {args.tenant_id} \
                    --app_secret {args.app_secret} \
                    --blob_storage_url {args.blob_storage_url} \
                    --blob_storage_inp_container {args.blob_storage_inp_container} \
                    --blob_storage_op_container {args.blob_storage_op_container}\""]
        
        batch_obj.add_tasks(args.image, "latest", job_id, 
                            commands)
        
        completed = \
            batch_obj\
            .wait_for_tasks_to_complete(job_id, 
                                        datetime.timedelta(minutes=30))
        
        if completed == 1:
            batch_obj.print_task_output(job_id)
        else:
            raise Exception("Timeout happened for task completion")
            
    except Exception as e:
        print(e)
    finally:
        batch_obj.delete_job(job_id)
        batch_obj.delete_pool(pool_id)
        pass
    