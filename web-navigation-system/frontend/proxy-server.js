const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();

// CORS中间件
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.sendStatus(200);
        return;
    }
    
    next();
});

// 静态文件服务
app.use(express.static(path.join(__dirname, 'public')));

// API代理
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5000',
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        console.log('代理请求:', req.method, req.url);
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log('代理响应:', proxyRes.statusCode, req.url);
    }
}));

// 启动服务器
app.listen(8017, () => {
    console.log('前端服务器运行在 http://localhost:8017');
    console.log('API代理到 http://localhost:5000');
});