from batch import Batch
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-k", "--batch_key", help="batch account key", type=str)
    parser.add_argument("-u", "--acr_user", help="acr username", type=str)
    parser.add_argument("-p", "--acr_pwd", help="acr password", type=str)
    parser.add_argument("-s", "--app_secret", help="client app secret", type=str)
    parser.add_argument("-a", "--app_id", help="client app id", type=str)
    parser.add_argument("-t", "--tenant_id", help="client tenant id", type=str)
    parser.add_argument("-f", "--pool_id", help="batch pool id", type=str)
    parser.add_argument("-r", "--batch_url", help="batch account url", type=str)
    parser.add_argument("-v", "--s_vm_size", help="scheduler VM type", type=str)
    parser.add_argument("-w", "--vm_size", help="pool VM type", type=str)
    parser.add_argument("-n", "--s_pool_count", help="scheduler node count", type=str)
    parser.add_argument("-i", "--image", help="docker image", type=str)
    parser.add_argument("-l", "--acr_url", help="acr url", type=str)
    parser.add_argument("-m", "--num_tasks", help="number of tasks in job", type=str)
    parser.add_argument("-x", "--blob_storage_url", help="Blob storage container URL", type=str)
    parser.add_argument("-y", "--blob_storage_inp_container", help="Blob storage container to store task inputs", type=str)
    parser.add_argument("-z", "--blob_storage_out_container", help="Blob storage container to store task outputs", type=str)
    parser.add_argument("-b", "--job_schedule_id", help="Job schedule id", type=str)
    parser.add_argument("-q", "--job_interval", help="Job interval in seconds", type=str)
      
    args = parser.parse_args()
    job_schedule_id = args.job_schedule_id
        
    batch_obj = Batch(args.batch_url, 
                      args.app_id, 
                      args.tenant_id, 
                      args.app_secret)
    
    try:
        command = f"/bin/bash -c \
            'cd /app && \
                JOB_ID=$(uuidgen) && \
                python create_tasks.py \
                    --job_id $JOB_ID \
                    --app_id {args.app_id} \
                    --tenant_id {args.tenant_id} \
                    --app_secret {args.app_secret} \
                    --blob_storage_url {args.blob_storage_url} \
                    --blob_storage_container {args.blob_storage_inp_container} && \
                python run_batch.py \
                    --job_id $JOB_ID \
                    --batch_key {args.batch_key} \
                    --acr_user {args.acr_user} \
                    --acr_pwd {args.acr_pwd} \
                    --app_secret {args.app_secret} \
                    --app_id {args.app_id} \
                    --tenant_id {args.tenant_id} \
                    --pool_id {args.pool_id} \
                    --batch_url {args.batch_url} \
                    --vm_size {args.vm_size} \
                    --pool_count {args.num_tasks} \
                    --image {args.image} \
                    --acr_url {args.acr_url} \
                    --num_tasks {args.num_tasks} \
                    --blob_storage_url {args.blob_storage_url} \
                    --blob_storage_inp_container {args.blob_storage_inp_container} \
                    --blob_storage_out_container {args.blob_storage_out_container}'"
        
        batch_obj.create_job_schedule(job_schedule_id, 
                                      args.s_vm_size, 
                                      args.s_pool_count, 
                                      float(args.job_interval),
                                      args.image, 
                                      "latest", 
                                      args.acr_url, 
                                      args.acr_user, 
                                      args.acr_pwd,
                                      command)
        
    except Exception as e:
        print(e)
        batch_obj.delete_job_schedule(job_schedule_id)
    