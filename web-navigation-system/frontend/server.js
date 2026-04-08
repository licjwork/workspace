const express = require('express');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = 8017;

// 请求日志中间件
app.use((req, res, next) => {
    console.log(`收到请求: ${req.method} ${req.url} from ${req.ip}`);
    next();
});

// CORS支持 - 解决移动端访问问题（必须在静态文件服务之前）
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, X-Session-Token');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    next();
});

// 解析JSON body
app.use(express.json());
// 解析URL编码的body
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use(express.static(path.join(__dirname, 'public')));
app.use('/admin', express.static(path.join(__dirname, '../admin')));

// API代理到后端 - 使用原生HTTP模块
app.use('/api', (req, res) => {
    console.log(`代理请求: ${req.method} ${req.url}`);
    console.log('请求头:', JSON.stringify(req.headers, null, 2));
    
    // 处理OPTIONS预检请求
    if (req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Origin', '*');
        res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        res.header('Access-Control-Allow-Headers', 'Content-Type, X-Session-Token');
        res.status(200).end();
        return;
    }
    
    const http = require('http');
    const options = {
        hostname: 'xiaoliyaooo.ltd',
        port: 80,
        path: `/api${req.url}`,
        method: req.method,
        headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'Frontend-Server',
            'Host': 'xiaoliyaooo.ltd'
        }
    };
    
    console.log('代理选项:', JSON.stringify(options, null, 2));
    
    // 传递X-Session-Token头
    if (req.headers['x-session-token']) {
        options.headers['X-Session-Token'] = req.headers['x-session-token'];
    }
    
    const proxyReq = http.request(options, (proxyRes) => {
        console.log('收到后端响应，状态码:', proxyRes.statusCode);
        let data = '';
        proxyRes.on('data', (chunk) => {
            data += chunk;
        });
        proxyRes.on('end', () => {
            console.log('响应数据长度:', data.length);
            res.status(proxyRes.statusCode).json(JSON.parse(data));
        });
    });
    
    proxyReq.on('error', (err) => {
        console.error('代理错误详情:', {
            message: err.message,
            code: err.code,
            stack: err.stack
        });
        res.status(500).json({ 
            error: '后端服务连接失败',
            details: err.message 
        });
    });
    
    // 如果有请求体，发送给后端
    if (req.body) {
        console.log('发送请求体，长度:', JSON.stringify(req.body).length);
        proxyReq.write(JSON.stringify(req.body));
    }
    
    proxyReq.end();
});

// 首页路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`前端服务器运行在 http://0.0.0.0:${PORT}`);
});