from azure.storage.blob import BlobServiceClient
import os
import helpers

class Blob:
    def __init__(self, 
                 storage_account_url, 
                 app_id:str=None, 
                 tenant_id:str=None, 
                 secret:str=None):
        """
        Blob init
        
        :param storage_account_url: blob storage account url
        :param app_id: client app id
        :param tenant_id: client tenant id
        :param secret: app client secret
        """
        credentials = \
            helpers.get_credentials(app_id, tenant_id, secret)
            
        self.blob_service_client = \
            BlobServiceClient(\
                account_url=f"https://{storage_account_url}",
                credential=credentials
            )
        
    def get_blob_client(self, container:str, blobPath:str):
        """
        Get blob client
        
        :param container: blob storage container name
        :param blobPath: path of blob w.r.t. container
        :returns: Blob client object
        """
        return self.blob_service_client\
            .get_blob_client(container, blobPath)
    
    def get_container_client(self, container:str):
        """
        Get blob container client
        
        :param container: blob storage container name
        :returns: Blob container client object
        """
        return self.blob_service_client\
            .get_container_client(container)

    def get_blob_stream(self, container:str, blobPath:str):
        """
        Read blob stream from blob storage
        
        :param container: blob storage container
        :param blobPath: blob storage file path w.r.t. container
        :returns: Blob stream
        """
        print(f'Getting blob from [{os.path.join(container, blobPath)}]...')
        
        blob_client = self.get_blob_client(container, blobPath)
        return blob_client.download_blob()

    def get_blob_list_in_container(self, container:str):
        """
        Get list of all blobs in a container

        :param container: The name of the Azure Blob storage container.
        """
        print(f'Getting blob list from [{container}]...')
        
        container_client = self.get_container_client(container)
        blob_list = container_client.list_blobs()
        
        result = [blob.name for blob in blob_list]
        
        return result

    def upload_file_to_container(self, 
                                 local_file_path:str, 
                                 output_container:str, 
                                 output_file_path:str):
        """
        Uploads a local file to an Azure Blob storage container.

        :param local_file_path: The local path to the file.
        :param output_container: The name of the Azure Blob storage container.
        :param output_file_path: The path to the file in blob storage w.r.t. container.
        """
        container_client = self.get_container_client(output_container)
        
        if not container_client.exists():
            container_client.create_container()
            
        blob_client = \
            self.get_blob_client(output_container, output_file_path)

        print(f'Uploading file {local_file_path} to container [{output_container}]...')

        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        