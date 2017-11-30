from cl.client.data import DataClient
from cl.log import configure_logger
from cl.cli.utils import get_files_in_directory

from cl.client.base import RussellHttpClient
import cl

cl.russell_host = "http://test.dl.russellcloud.com"
configure_logger(True)


class Test(RussellHttpClient):
    def test(self):
        upload_files, total_file_size = get_files_in_directory(path='.', file_type='data')
        self.request("POST",
                            "/data/",
                            data={'json': '{"version": 1, "module_type": "data", "name": "bike_sharing_dataset", "data_type": "dir", "description": "1"}'},
                            files=upload_files,
                            timeout=3600)



Test().test()
