# AI provider configuration

User confirmed Alibaba Cloud Bailian (Model Studio), model `kimi-k3.1-pro`.

Official reference: https://help.aliyun.com/zh/model-studio/kimi-api

The Beijing OpenAI-compatible base URL is `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`. User confirmed the exact account endpoint: `https://llm-mwp7k7j6crfxhdtn.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`. Do not replace it with Coding Plan endpoints or guess a workspace from a credential. Region and model access must match the account.

`AI_API_KEY` is backend-only, externally injected. No actual credential is stored in tracked or generated files. Phase 0 does not need a billable inference call. Model connectivity, Embedding/OCR selection, data policy and real AI evaluation belong to phase 2.
