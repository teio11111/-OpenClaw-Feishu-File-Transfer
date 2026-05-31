---
name: feishu-file-transfer
description: Send local computer files to Feishu/Lark through the Feishu Open Platform API.
---

# Feishu File Transfer Skill

This skill sends local files from a Windows computer to Feishu/Lark.

Use this skill when the user asks to send, upload, or transfer a local file to Feishu or Lark.

## What it does

1. Reads a local file path provided by the user.
2. Uses Feishu App ID and App Secret for authentication.
3. Uploads the file to Feishu.
4. Sends the uploaded file to a user or group chat.

## Required environment variables

powershell
$env:FEISHU_APP_ID="your_app_id"
$env:FEISHU_APP_SECRET="your_app_secret"
$env:FEISHU_RECEIVE_ID="your_open_id_or_chat_id"
$env:FEISHU_RECEIVE_ID_TYPE="open_id"
