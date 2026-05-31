# OpenClaw Feishu File Transfer Demo

This project demonstrates an OpenClaw Skill that sends local computer files to Feishu/Lark through the Feishu Open Platform API.

## Features

- Send local files from Windows to Feishu/Lark
- Support common file types such as `.txt`, `.docx`, `.pdf`, `.png`, and `.zip`
- Use Feishu App ID and App Secret for authentication
- Upload the file first, then send it to a user or chat

## Folder Structure

```text
Skills/
└── feishu-file-transfer/
    ├── SKILL.md
    ├── send_file_to_feishu.py
    ├── requirements.txt
    └── README.md
Security Notice

Do not upload App Secret, API keys, open_id, tokens, passwords, or private files to GitHub.

Use environment variables instead:

$env:FEISHU_APP_ID="your_app_id"
$env:FEISHU_APP_SECRET="your_app_secret"
$env:FEISHU_RECEIVE_ID="your_open_id_or_chat_id"
$env:FEISHU_RECEIVE_ID_TYPE="open_id"
Test Command
cd .\Skills\feishu-file-transfer
python -m pip install -r requirements.txt
python .\send_file_to_feishu.py "C:\Users\YourName\Desktop\test.txt" --app-id $env:FEISHU_APP_ID --app-secret $env:FEISHU_APP_SECRET --receive-id $env:FEISHU_RECEIVE_ID --receive-id-type open_id
Demo Result

A local file can be sent from a Windows computer to the Feishu mobile app through OpenClaw.
