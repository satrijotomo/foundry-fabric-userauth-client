# Foundry + Fabric User-Authenticated Python Client

This repo provides a ready-to-run Python client for:

- Authenticating an end user with Microsoft Entra ID using interactive browser sign-in
- Calling a published Azure AI Foundry agent through the **Responses** protocol
- Calling a published Azure AI Foundry agent through the **Activity** protocol
- Optionally calling a **Fabric data agent directly** using the same signed-in user identity

## Why this repo exists

Microsoft documents that external Python apps can consume **Fabric data agents** using **interactive browser authentication**, and the data agent runs with the **signed-in user’s permissions**. Microsoft also documents that published Foundry agents can be invoked via the **Responses** and **Activity** protocols. 【1-a6d7ea】【2-6ed868】【3-4b5991】

This repo gives you a practical pattern to test both paths in one place.

## Important limitation

This repo supports:

1. Calling your Foundry agent endpoint with a signed-in user
2. Calling a Fabric data agent directly with the same signed-in user

However, the sourced Microsoft documentation used here does **not explicitly confirm** that a delegated user token sent to the Foundry `/responses` endpoint is automatically forwarded to an embedded Fabric data agent tool inside that Foundry agent. Because of that, the direct Fabric call is included as the **documented user-authenticated path**. 【1-a6d7ea】【2-6ed868】

## Repo structure

```text
foundry-fabric-userauth-client/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── auth.py
│   ├── foundry_client.py
│   ├── fabric_client.py
│   └── main.py
└── samples/
    └── activity_payload.json


