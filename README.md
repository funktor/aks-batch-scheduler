# az-batch-scheduler
Run Spark and non-Spark jobs with Azure Batch

# Steps for running jobs without scheduling (Ubuntu + Bash)
1. Generate an unique job id from command line : 
```JOB_ID=$(uuidgen)```

2. Build and push the base docker image : 
```./containerize_batch_base.sh --registry acr_registry_username.azurecr.io```

3. Build and push the docker image for your task : 
```./containerize_batch.sh --registry acr_registry_username.azurecr.io --image task_acr_image_name --dockerpath Dockerfile.batch```

4. Create task(s) : 
```python3 create_tasks.py \
    --job_id $JOB_ID \
    --app_id APP_ID \
    --tenant_id TENANT_ID \
    --app_secret APP_SECRET \
    --blob_storage_url BLOB_STORAGE_URL \
    --blob_storage_container BLOB_INPUT_CONTAINER```

5. Run batch
```python3 run_batch.py \
    --job_id $JOB_ID \
    --batch_key BATCH_ACCOUNT_KEY \
    --acr_user ACR_USERNAME \
    --acr_pwd ACR_PASSWORD \
    --app_secret APP_SECRET \
    --tenant_id TENANT_ID \
    --pool_id POOL_ID \
    --batch_url BATCH_ACCOUNT_URL \
    --vm_size VM_SIZE \
    --pool_count POOL_SIZE \
    --image TASK_IMAGE_NAME \
    --acr_url ACR_ACCOUNT_URL \
    --num_tasks NUM_TASKS \
    --blob_storage_url BLOB_STORAGE_URL \
    --blob_storage_inp_container BLOB_INPUT_CONTAINER \
    --blob_storage_out_container BLOB_OUTPUT_CONTAINER```
