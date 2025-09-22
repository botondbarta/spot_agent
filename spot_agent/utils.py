import requests
import yaml
from ai2thor.controller import Controller
from dotmap import DotMap


def get_config_from_yaml(yaml_file):
    with open(yaml_file, 'r') as config_file:
        config_yaml = yaml.load(config_file, Loader=yaml.FullLoader)
    # Using DotMap we will be able to reference nested parameters via attribute such as x.y instead of x['y']
    config = DotMap(config_yaml, _dynamic=False)
    return config


def shutdown_server(api_base: str, model_id: str = "qwen2.5-coder:32b") -> None:
    requests.post(
        f"{api_base}/api/generate",
        json={
            "model": model_id,
            "keep_alive": 0,  # unload after use
            "stream": False  # easier to work with in script
        }
    )


def get_controller():
    return Controller(
        quality='High WebGL',
        # agentMode="locobot",
        visibilityDistance=0.5,
        scene="FloorPlan25",
        gridSize=0.25,
        movementGaussianSigma=0.005,
        rotateStepDegrees=90,
        rotateGaussianSigma=0.5,
        # renderDepthImage=False,
        # renderInstanceSegmentation=False,
        width=900,
        height=900,
        fieldOfView=70,
    )
