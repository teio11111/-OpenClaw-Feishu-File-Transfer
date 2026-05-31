import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path

import requests


FEISHU_HOST = "https://open.feishu.cn"


class FeishuFileTransferError(Exception):
    """Custom error for Feishu file transfer failures."""


def get_required_value(cli_value: str | None, env_name: str, display_name: str) -> str:
    value = cli_value or os.getenv(env_name)
    if not value:
        raise FeishuFileTransferError(
            f"缺少 {display_name}。请通过命令参数或环境变量 {env_name} 提供。"
        )
    return value


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = f"{FEISHU_HOST}/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise FeishuFileTransferError(f"请求飞书 token 接口失败：{exc}") from exc

    data = response.json()
    if data.get("code") != 0:
        raise FeishuFileTransferError(f"获取 token 失败：{data}")

    return data["tenant_access_token"]


def guess_file_type(file_path: Path) -> str:
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return "pdf"
    if ext in {".doc", ".docx"}:
        return "doc"
    if ext in {".xls", ".xlsx", ".csv"}:
        return "xls"
    if ext in {".ppt", ".pptx"}:
        return "ppt"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}:
        return "image"

    return "stream"


def validate_file(file_path: Path, max_size_mb: int) -> int:
    if not file_path.exists():
        raise FeishuFileTransferError(f"文件不存在：{file_path}")
    if not file_path.is_file():
        raise FeishuFileTransferError(f"不是普通文件：{file_path}")

    file_size = file_path.stat().st_size
    if file_size <= 0:
        raise FeishuFileTransferError("不能上传空文件。")

    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise FeishuFileTransferError(
            f"文件大小为 {file_size / 1024 / 1024:.2f}MB，超过当前限制 {max_size_mb}MB。"
        )

    return file_size


def upload_file(token: str, file_path: Path, max_size_mb: int) -> str:
    validate_file(file_path, max_size_mb)

    file_name = file_path.name
    file_type = guess_file_type(file_path)
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = "application/octet-stream"

    url = f"{FEISHU_HOST}/open-apis/im/v1/files"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with file_path.open("rb") as file_obj:
            files = {"file": (file_name, file_obj, mime_type)}
            data = {"file_type": file_type, "file_name": file_name}
            response = requests.post(
                url,
                headers=headers,
                data=data,
                files=files,
                timeout=60,
            )
            response.raise_for_status()
    except requests.RequestException as exc:
        raise FeishuFileTransferError(f"请求飞书上传文件接口失败：{exc}") from exc

    result = response.json()
    if result.get("code") != 0:
        raise FeishuFileTransferError(f"上传文件失败：{result}")

    return result["data"]["file_key"]


def send_file_message(
    token: str,
    receive_id: str,
    file_key: str,
    receive_id_type: str,
) -> dict:
    url = f"{FEISHU_HOST}/open-apis/im/v1/messages"
    params = {"receive_id_type": receive_id_type}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key}, ensure_ascii=False),
    }

    try:
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise FeishuFileTransferError(f"请求飞书发送消息接口失败：{exc}") from exc

    result = response.json()
    if result.get("code") != 0:
        raise FeishuFileTransferError(f"发送文件消息失败：{result}")

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="通过飞书把电脑本地文件发送到手机端。"
    )
    parser.add_argument("file", help="要发送的本地文件路径")
    parser.add_argument("--app-id", help="飞书应用 App ID，也可用 FEISHU_APP_ID")
    parser.add_argument("--app-secret", help="飞书应用 App Secret，也可用 FEISHU_APP_SECRET")
    parser.add_argument("--receive-id", help="接收方 ID，也可用 FEISHU_RECEIVE_ID")
    parser.add_argument(
        "--receive-id-type",
        choices=["chat_id", "open_id", "user_id", "union_id", "email"],
        help="接收方 ID 类型，也可用 FEISHU_RECEIVE_ID_TYPE，默认 chat_id",
    )
    parser.add_argument(
        "--max-size-mb",
        type=int,
        default=30,
        help="允许上传的最大文件大小，默认 30MB",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        app_id = get_required_value(args.app_id, "FEISHU_APP_ID", "App ID")
        app_secret = get_required_value(args.app_secret, "FEISHU_APP_SECRET", "App Secret")
        receive_id = get_required_value(args.receive_id, "FEISHU_RECEIVE_ID", "接收方 ID")
        receive_id_type = args.receive_id_type or os.getenv("FEISHU_RECEIVE_ID_TYPE", "chat_id")

        file_path = Path(args.file).expanduser().resolve()

        print("正在获取飞书 token...")
        token = get_tenant_access_token(app_id, app_secret)

        print("正在上传文件...")
        file_key = upload_file(token, file_path, args.max_size_mb)

        print("正在发送到飞书...")
        send_file_message(token, receive_id, file_key, receive_id_type)

        print("发送成功！请在手机端飞书中查看文件。")
        return 0

    except Exception as exc:
        print(f"执行失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

