import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

import httpx


def _find_chat_id(session_id: str) -> str | None:
    """从 sessions.json 反查 chat_id"""
    sessions_file = Path.home() / ".hermes" / "sessions" / "sessions.json"
    if not sessions_file.exists():
        return None
    try:
        data = json.loads(sessions_file.read_text())
    except Exception:
        return None
    for entry in data.values():
        if entry.get("session_id") == session_id:
            origin = entry.get("origin") or {}
            return origin.get("chat_id")
    return None


def _load_session(session_id: str) -> dict | None:
    """加载 session JSON 文件"""
    session_file = Path.home() / ".hermes" / "sessions" / f"session_{session_id}.json"
    if not session_file.exists():
        return None
    try:
        return json.loads(session_file.read_text())
    except Exception:
        return None


def _format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m{int(seconds % 60)}s"
    else:
        h = int(seconds / 3600)
        m = int((seconds % 3600) / 60)
        return f"{h}h{m}m"


def _build_status_line(status: str, session: dict) -> str:
    """构造极简 emoji 状态行"""
    model = session.get("model", "?").split("/")[-1]  # 取短名
    message_count = session.get("message_count", 0)
    messages = session.get("messages", [])
    session_start = session.get("session_start", "")
    last_updated = session.get("last_updated", "")

    # 会话时长
    duration_str = ""
    if session_start and last_updated:
        try:
            fmt = "%Y-%m-%dT%H:%M:%S.%f"
            start_dt = datetime.strptime(session_start[:26], fmt)
            end_dt = datetime.strptime(last_updated[:26], fmt)
            duration = (end_dt - start_dt).total_seconds()
            duration_str = _format_duration(duration)
        except Exception:
            pass

    # 工具调用次数
    tool_calls = sum(
        1
        for m in messages
        if m.get("role") == "assistant" and m.get("tool_calls")
    )

    parts = [status, f"🧠{model}", f"💬{message_count}"]
    if duration_str:
        parts.append(f"⏱️{duration_str}")
    if tool_calls:
        parts.append(f"🔧{tool_calls}")

    return " ".join(parts)


async def _send_feishu(chat_id: str, text: str) -> None:
    """发送飞书文本消息"""
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        return

    async with httpx.AsyncClient(timeout=10) as client:
        token_resp = await client.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": app_id, "app_secret": app_secret},
        )
        token = token_resp.json().get("tenant_access_token")
        if not token:
            return

        await client.post(
            "https://open.feishu.cn/open-apis/im/v1/messages",
            headers={"Authorization": f"Bearer {token}"},
            params={"receive_id_type": "chat_id"},
            json={
                "receive_id": chat_id,
                "msg_type": "text",
                "content": json.dumps({"text": text}),
            },
        )


async def handle(event_type, context):
    if event_type != "agent:end":
        return

    platform = context.get("platform", "")
    session_id = context.get("session_id", "")
    response = context.get("response", "")

    asyncio.create_task(
        _send_delayed_notification(platform, session_id, response)
    )


async def _send_delayed_notification(platform, session_id, response) -> None:
    """后台任务：延迟 3 秒后发送极简状态"""
    await asyncio.sleep(3)

    failed = any(k in response for k in ("⚠️", "❌", "failed", "encountered an error"))
    status = "⚠️" if failed else "✅"

    session = _load_session(session_id) or {}
    line = _build_status_line(status, session)

    if platform == "feishu":
        chat_id = _find_chat_id(session_id)
        if chat_id:
            await _send_feishu(chat_id, line)
    elif platform in ("cli", "tui"):
        print(f"[task_done] {line}")
    else:
        pass
