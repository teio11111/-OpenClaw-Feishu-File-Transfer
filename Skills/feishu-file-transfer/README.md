# OpenClaw 飞书文件传输 Skill 演示

本项目是一个 OpenClaw Skill 示例，用于演示如何通过 OpenClaw 调用本地脚本，并借助飞书开放平台 API，把电脑本地文件发送到飞书/Lark。

这个项目主要用于展示 OpenClaw 不只是聊天工具，而是可以作为 Agent 调用外部工具、执行本地任务，并把结果发送到其他应用。

---

## 项目功能

- 支持从 Windows 本地发送文件到飞书
- 支持常见文件类型，例如 `.txt`、`.docx`、`.pdf`、`.png`、`.zip`
- 使用飞书 App ID 和 App Secret 进行认证
- 通过环境变量保存敏感信息，避免把密钥写进代码
- 先上传文件到飞书，再发送给指定用户或群聊

---

## 项目结构

```text
Skills/
└── feishu-file-transfer/
    ├── README.md
    ├── SKILL.md
    ├── send_file_to_feishu.py
    └── requirements.txt

电脑本地文件
↓
OpenClaw Skill 调用 Python 脚本
↓
飞书开放平台 API 上传文件
↓
飞书手机端收到文件

项目总结

这个项目展示了 OpenClaw 的基础 Agent 能力：
用户不只是和模型聊天，而是可以让 OpenClaw 调用本地工具，操作文件，并和外部应用进行交互。

通过这个 Skill，OpenClaw 可以把本地文件发送到飞书，从而实现简单的跨平台文件传输自动化。
