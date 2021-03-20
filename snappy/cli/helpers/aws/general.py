import json
from typing import Any, Dict, Optional

from botocore.response import StreamingBody
from snappy.cli.config import IAMClient


def get_role_arn_by_name(name: str, marker: Optional[str] = None) -> str:
    if not marker:
        roles = IAMClient.list_roles()
    else:
        roles = IAMClient.list_roles(Marker=marker)

    for role in roles["Roles"]:
        if role["RoleName"] == name:
            return role["Arn"]

    if roles["IsTruncated"]:
        marker = roles["Marker"]
        get_role_arn_by_name(name, marker=marker)
    else:
        raise ValueError(f"Name {name} not found.")


def decode_streaming_body_payload(streaming_body: StreamingBody) -> Dict[str, Any]:
    return json.loads(streaming_body.read().decode("utf-8"))
