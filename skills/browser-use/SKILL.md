# 浏览器使用技能 (Browser Use Skill)

浏览器使用技能是一个通用的网页自动化工具，基于 CDP (Chrome DevTools Protocol) 协议，允许通过浏览器执行导航、点击、输入和内容抓取等操作。

## 功能特性

- ✅ **网页导航**：支持跳转到任意指定的 URL。
- ✅ **内容抓取**：支持提取页面的文本内容或 HTML 源码。
- ✅ **交互操作**：支持对页面元素进行点击、输入文本。
- ✅ **JS 执行**：支持在页面上下文中执行自定义的 JavaScript 代码。
- ✅ **分步控制**：通过命令行参数精确控制每一步操作。

## 使用方法

使用命令: `python3 skills/browser-use/scripts/browser_controller.py --action <动作> --url "<链接>" [其他参数]`

### 常用动作说明

1. **导航并抓取文本**：
   `python3 skills/browser-use/scripts/browser_controller.py --action scrape --url "https://example.com"`

2. **点击元素**：
   `python3 skills/browser-use/scripts/browser_controller.py --action click --url "https://example.com" --selector "#submit-button"`

3. **输入文本**：
   `python3 skills/browser-use/scripts/browser_controller.py --action type --url "https://example.com" --selector "input[name='q']" --text "搜索内容"`

4. **执行自定义 JS**：
   `python3 skills/browser-use/scripts/browser_controller.py --action evaluate --url "https://example.com" --js "window.scrollTo(0, 500)"`

## 技术实现

### 前置依赖

该技能依赖以下环境：
1. **VNC 服务器**：提供浏览器显示环境（通常为 `:1`，端口 5901）。
2. **浏览器环境**：Chromium 需运行在 VNC 显示桌面上，并开启 `--remote-debugging-port=18800`。
3. **Python 依赖**：`requests`, `websocket-client`。

#### 推荐启动方式
```bash
# 1. 启动 VNC (如果尚未启动)
vncserver :1 -geometry 1280x800 -depth 24
export DISPLAY=:1

# 2. 启动带调试端口的浏览器
/snap/bin/chromium --no-sandbox --remote-debugging-port=18800 --remote-allow-origins=* --disable-gpu --no-first-run
```

### 浏览器交互细节

- **CDP 连接**：脚本通过 `http://localhost:18800/json/list` 获取 WebSocket 调试地址。
- **元素选择器**：默认使用标准 CSS 选择器。
- **输入模拟**：通过 `Runtime.evaluate` 执行 JS 来修改 `value` 并触发 `input` 事件，确保能够被现代前端框架识别。

## 故障排除

- **无法连接到浏览器**：检查是否已启动带调试端口的浏览器（通常在 VNC :1 中）。
- **元素未找到**：检查选择器是否正确，或者页面是否尚未加载完成（脚本默认有简单的等待逻辑）。
- **执行超时**：对于大型页面，可能需要手动增加等待时间。

## 重要提醒

- **本技能参考了微博发布技能的实现逻辑**。
- **建议在操作前先用 `scrape` 查看页面结构**。
- **核心逻辑封装在 `browser_controller.py` 中，方便其他技能调用或扩展**。
