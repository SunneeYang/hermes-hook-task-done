# hermes-hook-task-done

Hermes Agent 任务完成通知 hook。

监听 `agent:end` 事件，任务结束后发送极简状态：
- ✅/⚠️ 成功或失败
- 使用模型（短名）
- 消息数
- 会话时长
- 工具调用次数

当前仅支持 **飞书**。

## 环境要求

- Hermes gateway 必须在运行中（`hermes gateway run`）
- 环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
- Python 包 `httpx`（Hermes 环境通常已存在）

## 安装

```bash
# 默认 profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/install.sh | bash

# 指定 profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/install.sh | bash -s -- <profile-name>
```

> ⚠️ **安装后需要重启 gateway**：
> ```bash
> hermes gateway restart
> ```

## 卸载

```bash
# 默认 profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/uninstall.sh | bash

# 指定 profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/uninstall.sh | bash -s -- <profile-name>
```

> ⚠️ **卸载后需要重启 gateway**，才能从内存中清除旧的 handler。

## 注意事项

- 本 hook **仅在 gateway 模式下生效**。单独运行 `hermes` 启动的 CLI/TUI 模式不会触发 `agent:end` 事件。
- 通知通过飞书 OpenAPI 发送，延迟 3 秒以确保出现在正文之后。

## 文件说明

| 文件 | 作用 |
|------|------|
| `HOOK.yaml` | Hook 清单（名称、事件） |
| `handler.py` | 事件处理逻辑 |
| `install.sh` | 一键安装脚本 |
| `uninstall.sh` | 一键卸载脚本 |

## 授权

MIT
