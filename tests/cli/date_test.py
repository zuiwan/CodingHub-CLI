from cl.client.experiment import ExperimentClient


experiment = ExperimentClient().get("68412e47b6b340bfbc52900b6d260e42")

print experiment.created_pretty

