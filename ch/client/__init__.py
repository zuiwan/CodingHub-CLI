import sys
import os
import tarfile
import zipfile
import requests
import ch
from ch.manager.auth_config import AuthConfigManager
from ch.log import logger
from ch.exceptions import (
    AuthenticationException,
    InvalidResponseException,
    NotFoundException,
    BadRequestException,
    ExistedException
)


class RussellHttpClient(object):
    """
    Base client for all HTTP operations
    """

    def __init__(self):
        self.base_url = ch.russell_host + "/api/v{}"
        self.access_token = AuthConfigManager.get_access_token()

    def request(self, method, url, params=None, data=None, json=None, files=None, access_token=None,
                auth=None, timeout=5, stream=False, api_version=1):
        """
        Execute the request using requests library
        """
        request_url = self.base_url.format(api_version) + url
        logger.debug("Starting request to url: {} with params: {}, data: {}".format(request_url, params, data))
        headers = {}
        if access_token:
            headers = {"Authorization": "Basic {}".format(access_token)}
        elif not auth:
            headers = {"Authorization": "Basic {}".format(
                self.access_token.token if self.access_token else None)
            }

        try:
            response = requests.request(method=method,
                                        url=request_url,
                                        params=params,
                                        headers=headers,
                                        data=data,
                                        json=json,
                                        files=files,
                                        timeout=timeout,
                                        stream=stream,
                                        auth=auth)
        except requests.exceptions.ConnectionError:
            sys.exit("Cannot connect to the Russell server. Check your internet connection.")
        if not stream:
            try:
                logger.debug("Response Content: {}, Headers: {}".format(response.json(), response.headers))
            except Exception:
                logger.debug("Request failed. Response: {}".format(response.content))
            try:
                self.check_response_status(response)
            except Exception as e:
                raise e
            else:
                result = response.json().get("data", "")
                return result
        else:
            logger.debug('HTTP Stream Request/Response...')
            try:
                self.check_response_status(response)
            except Exception as e:
                raise e
            else:
                return response

    def check_response_status(self, response):
        """
        Check if response is successful. Else raise Exception.
        """
        # 处理流式响应
        if not response.headers.get('Content-Type') in ('application/json', 'text/html'):
            return
        # 处理标准HTTP错误码
        if not (200 <= response.status_code < 300):
            if response.status_code == 401:
                raise AuthenticationException()
            elif response.status_code == 404:
                raise NotFoundException()
            else:
                raise InvalidResponseException()
        try:
            resp_json = response.json()
        except Exception as e:
            logger.debug(str(e))
            raise InvalidResponseException()

        # 处理自定义错误码
        code = resp_json.get("code", 500)
        if not (200 <= code < 300):
            try:
                message = resp_json.get("data")
            except Exception as e:
                logger.debug(str(e))
                message = None
            logger.debug("Error received : status_code: {}, message: {}"
                         .format(code, message or response.content))
            if code == 404:
                raise NotFoundException()
            elif code == 401:
                raise AuthenticationException()
            elif code == 400:
                raise BadRequestException()
            else:
                raise InvalidResponseException()

    def download(self, url, filename, timeout=10, api_version=1):
        """
        Download the file from the given url at the current path
        """
        logger.debug("Downloading file from url: {}".format(url))

        try:
            response = self.request(method='GET',
                                    url=url,
                                    stream=True,
                                    timeout=timeout,
                                    api_version=api_version)
            self.check_response_status(response)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return filename
        except requests.exceptions.ConnectionError as exception:
            logger.debug("Exception: {}".format(exception))
            sys.exit("Cannot connect to the Russell server. Check your internet connection.")

    def download_compressed(self, url, compression='tar', uncompress=True, delete_after_uncompress=False, dir=None,
                            api_version=1):
        """
        Download and optionally uncompress the tar file from the given url
        """
        if dir:
            if os.path.exists(dir):
                raise ExistedException
            else:
                os.mkdir(dir)
                os.chdir(dir)
        try:
            logger.info("Downloading the tar file to the current directory ...")
            filename = self.download(url=url, filename='output', api_version=api_version)
            if filename and os.path.isfile(filename) and uncompress:
                logger.info("Uncompressring the contents of the file ...")
                if compression == 'tar':
                    tar = tarfile.open(filename)
                    tar.extractall()
                    tar.close()
                elif compression == 'zip':
                    zip = zipfile.ZipFile(filename)
                    zip.extractall()
                    zip.close()
            if delete_after_uncompress:
                logger.info("Cleaning up the compressed file ...")
                os.remove(filename)
            return filename
        except requests.exceptions.ConnectionError as e:
            logger.error("Download ERROR! {}".format(e))
            return False
