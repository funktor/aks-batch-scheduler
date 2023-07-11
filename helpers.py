import os
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient

def get_credentials(app_id:str=None, 
                    tenant_id:str=None, 
                    secret:str=None):
    """
    Get azure credentials to be used with azure python sdk. 
    Uses spot pricing AAD app for authentication.
    
    :param app_id: client app id
    :param tenant_id: client tenant id
    :param secret: app client secret
    :returns: Credential object
    """
    
    os.environ\
    .update({\
        'AZURE_CLIENT_ID':app_id, 
        'AZURE_TENANT_ID':tenant_id, 
        'AZURE_CLIENT_SECRET':secret
    })
        
    return EnvironmentCredential()

def get_key_vault_secret(app_id:str, 
                         tenant_id:str, 
                         client_secret:str, 
                         key_vault_uri:str,
                         kv_secret:str):
    """
    Get azure key vault secret value
    
    :param app_id: client app id
    :param tenant_id: client tenant id
    :param client_secret: app client secret
    :param key_vault_uri: key-vault URI
    :param kv_secret: key-value store key
    :returns: KV secret value
    """
    credential = get_credentials(app_id, tenant_id, client_secret)
    secret_client = \
        SecretClient(vault_url=key_vault_uri, 
                     credential=credential)
        
    return secret_client.get_secret(kv_secret).value