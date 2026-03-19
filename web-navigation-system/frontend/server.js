const express = require('express');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = 8017;

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

// API代理到后端
app.use('/api', async (req, res) => {
    try {
        console.log(`代理请求: ${req.method} ${req.url}`);
        
        // 构建请求头，传递所有原始请求头
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // 传递X-Session-Token头（关键修复）
        if (req.headers['x-session-token']) {
            headers['X-Session-Token'] = req.headers['x-session-token'];
        }
        
        const response = await axios({
            method: req.method,
            url: `http://82.156.52.192:5000/api${req.url}`,
            data: req.body,
            headers: headers
        });
        res.status(response.status).json(response.data);
    } catch (error) {
        console.error('代理错误:', error.message);
        res.status(500).json({ 
            error: '后端服务连接失败',
            details: error.message 
        });
    }
});

// 首页路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`前端服务器运行在 http://0.0.0.0:${PORT}`);
});