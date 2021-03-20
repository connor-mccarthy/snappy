import os

LIBRARY_NAME = "snappy"

APP_FILE = "app.py"
REQUIREMENTS_FILE = "requirements.txt"
YAML_FILE = "snappy.yaml"
DOCKERFILE = os.path.join(os.path.dirname(__file__), "Dockerfile")

LAMBDA_PORTS = {"8080/tcp": 9000}
PYTHON_LAMBDA_BASE_IMAGE = "public.ecr.aws/lambda/python:3.7"
LOCAL_ENDPOINT = "http://localhost:9000/2015-03-31/functions/function/invocations"
HEADERS = {"Content-Type": "text/plain"}
DEFAULT_PAYLOAD = "{}"
DEFAULT_IMAGE_TAG = "latest"

DEFAULT_IMAGE_NAME = "snappy_lambda_image"
DEFAULT_CONTAINER_NAME = "snappy_lambda_container"

INFORMAL_LOCAL_CONTAINER_NAME = "Lambda container"
INFORMAL_LOCAL_IMAGE_NAME = "Lambda image"

LAMBDA_NAME_REQUIREMENTS = (
    "Use only letters, numbers, hyphens, or underscores with no spaces."
)

ECR_NAME_REQUIREMENTS = "The name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, and forward slashes."

HEALTCHECK_RESPONSE = {"healthcheck": "success"}
