import yaml

def load_config(key):
    with open('/etc/nan.d/provenance.yaml') as f:
        # noinspection PyUnresolvedReferences
        GD[key] = yaml.safe_load(f)
