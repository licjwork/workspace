# OpenClaw Provider & Model 配置模板

## 基础配置格式

在 `~/.openclaw/openclaw.json` 文件的 `models.providers` 部分添加新的provider。

### 1. Provider 配置模板

```json
"provider-name": {
  "baseUrl": "https://api.example.com/v1",
  "apiKey": "your-api-key-here",
  "api": "openai-completions",
  "models": [
    {
      "id": "model-id",
      "name": "Model Display Name (Provider Name)",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": {
        "input": 0,
        "output": 0,
        "cacheRead": 0,
        "cacheWrite": 0
      },
      "contextWindow": 32768,
      "maxTokens": 8192
    }
  ]
}
```

### 2. Model 参数说明

- **id**: 模型唯一标识符（provider/format）
- **name**: 显示名称
- **api**: API类型（通常是 "openai-completions"）
- **reasoning**: 是否支持推理（true/false）
- **input**: 输入类型数组
  - `"text"`: 文本输入
  - `"image"`: 图像输入
- **cost**: 成本配置（暂时都设为0）
- **contextWindow**: 上下文窗口大小
- **maxTokens**: 最大输出token数

### 3. 多模态模型配置示例

```json
{
  "id": "provider/multimodal-model",
  "name": "Multimodal Model (Provider)",
  "api": "openai-completions",
  "reasoning": false,
  "input": ["text", "image"],
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "contextWindow": 32768,
  "maxTokens": 4096
}
```

### 4. 默认模型配置

在 `agents.defaults.model` 部分设置默认模型：

```json
"model": {
  "primary": "provider-name/model-id",
  "fallbacks": [
    "another-provider/model-id",
    "backup-provider/model-id"
  ]
}
```

### 5. 模型详细配置

在 `agents.defaults.models` 中为特定模型添加配置：

```json
"provider-name/model-id": {
  "streaming": true
}
```

## 现有配置参考

你可以参考现有配置：
- NVIDIA API: `custom-integrate-api-nvidia-com`
- LongCat API: `custom-api-longcat-chat`
- BigModel API: `custom-bigmodel-api`

## 配置完成后

1. 将你的配置发给我
2. 我会帮你合并到 `openclaw.json` 中
3. 重启OpenClaw服务使配置生效

请按照这个模板整理你要添加的provider和model配置。