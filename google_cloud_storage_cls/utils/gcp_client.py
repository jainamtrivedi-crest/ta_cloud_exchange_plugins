"""
BSD 3-Clause License

Copyright (c) 2021, Netskope OSS
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""GCP client class."""


import time
import json
import uuid
from google.cloud import storage


class GCPClient:
    """GCP Client Class."""

    def __init__(self, configuration, logger):
        """Init method."""
        self.configuration = configuration
        self.logger = logger

    def get_gcp_client(self):
        """To get gcp client."""
        try:
            key = json.loads(self.configuration["key_file"])
            client = storage.Client.from_service_account_info(key)
            return client
        except json.decoder.JSONDecodeError as err:
            self.logger.error(
                f"GCP Storage Plugin: Error occurred while decoding JSON key: {err}"
            )
            raise
        except Exception:
            raise

    def get_bucket(self):
        """To get bucket if exists."""
        try:
            client = self.get_gcp_client()
            bucket_name = self.configuration["bucket_name"]
            bucket = client.get_bucket(bucket_name)
            return bucket
        except Exception as e:
            self.logger.error(f"Error occurred while getting bucket: {e}")
            raise

    def push(self, file_name, data_type, subtype):
        """Push method."""
        cur_time = int(time.time())
        if data_type is None:
            object_name = f'{self.configuration["obj_prefix"]}_webtx_{cur_time}_{str(uuid.uuid1())}'
        else:
            object_name = f'{self.configuration["obj_prefix"]}_{data_type}_{subtype}_{cur_time}_{str(uuid.uuid1())}'
        try:
            bucket = self.get_bucket()
            blob_object = bucket.blob(object_name)
            blob_object.upload_from_filename(filename=file_name)
            self.logger.info(
                f"Successfully Uploaded to GCP Storage as blob file. {object_name}"
            )
        except Exception as e:
            self.logger.error(f"Error occurred while Pushing data object: {e}")
            raise
