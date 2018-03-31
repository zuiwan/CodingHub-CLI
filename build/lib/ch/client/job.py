import json

from ch.client import RussellHttpClient
from ch.manager.experiment_config import ExperimentConfigManager
from ch.model.job import JobReq, JobSpecification
from kafka import KafkaConsumer


class ExperimentClient(RussellHttpClient):
    """
    Client to interact with Experiments api
    """

    def __init__(self):
        self.url = "/job/{id}"
        super(ExperimentClient, self).__init__()

    def get_all(self):
        experiment_config = ExperimentConfigManager.get_config()
        experiments_dict = self.request("GET",
                                        self.url,
                                        params="family_id={}".format(experiment_config.family_id))
        return [expt for expt in experiments_dict]

    def get(self, id):
        experiment_dict = self.request("GET",
                                       url=self.url.format(id=id))
        return experiment_dict

    def stop(self, id):
        self.request("POST",
                     url=self.url.format(id=id),
                     params={'action': 'stop'})
        return True

    def create(self, experiment_request):
        response = self.request("POST",
                                url="/experiment/run",
                                data=json.dumps(experiment_request.to_dict()),
                                timeout=3600)
        return response.get("id")

    def delete(self, id):
        self.request("DELETE",
                     "/experiment/{}".format(id))
        return True

    def get_log_server(self, id):
        log_dict = self.request("GET",
                                "/task/{}/log".format(id))
        if log_dict.get('method') == 'kafka':
            return log_dict.get('server')
        return None

    def get_log_stream_container(self, id, method='kafka'):
        log_server = self.get_log_server(id)
        if not log_server:
            return
        try:
            consumer = KafkaConsumer(id,
                                     bootstrap_servers=log_server,
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=False,
                                     request_timeout_ms=40000,
                                     consumer_timeout_ms=10000)
        except:
            yield "Get log in container failed"
            return
        else:
            try:
                for msg in consumer:
                    yield json.loads(msg.value.decode('utf-8')).get("log").strip("\n")
            except StopIteration as e:
                return

    def get_task_detail(self, id):
        url = "/task/%s" % id
        response = self.request("GET",
                                url=url,
                                params={"content": "detail"})
        return response

    def get_task_url(self, id):
        res = self.get_task_detail(id)
        if isinstance(res, dict):
            return dict(jupyter_url=res.get('jupyter_url'),
                        tensorboard_url=res.get('tensorboard_url'))
        else:
            return dict()

    def submit(self, jobId, jobReq):
        url = self.url.format(id=jobId) + "/submit"
        self.request(method="POST",
                     url=url,
                     json=jobReq.to_dict())
