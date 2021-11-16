
#
# oci-vault-get-secret-python version 1.0.
#
# Copied and updated the code by Tanveer Iqbal
# All right reserved by Fundi-app
#

import io
import json
import base64
import oci
import logging


from fdk import response

def get_text_secret(secret_ocid):
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        client = oci.secrets.SecretsClient({}, signer=signer)
        secret_content = client.get_secret_bundle(secret_ocid).data.secret_bundle_content.content.encode('utf-8')
        decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    except Exception as ex:
        print("ERROR: failed to retrieve the secret content", ex, flush=True)
        raise
    return decrypted_secret_content


def handler(ctx, data: io.BytesIO=None):
    logging.getLogger().info("function start")

    secret_ocid = secret_type = db_password = ""
    try:
        cfg = dict(ctx.Config())
        secret_ocid = cfg["secret_ocid"]
        logging.getLogger().info("Secret ocid = " + secret_ocid)
        secret_type = cfg["secret_type"]
        logging.getLogger().info("Secret type = " + secret_type)

    except Exception as e:
        print('ERROR: Missing configuration keys, secret ocid and secret_type', e, flush=True)
        raise

    if secret_type == "text":
        db_password = get_text_secret(secret_ocid)
    else:
        raise ValueError('the value of the configuration parameter "secret_type" has to be either "text" or "binary"')

    logging.getLogger().info("function end")
    return response.Response(
        ctx, 
        response_data=json.dumps({ "db_password": db_password }),
        headers={"Content-Type": "application/json"}
    )
