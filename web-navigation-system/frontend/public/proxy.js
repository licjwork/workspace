// 代理配置，让前端能访问到后端API
const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});

const server = http.createServer(function(req, res) {
    // 设置CORS头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // 代理API请求到后端
    if (req.url.startsWith('/api/')) {
        proxy.web(req, res, { target: 'http://localhost:5000' });
    } else {
        // 静态文件服务
        require('http-server').createServer({
            root: './public',
            cache: 3600
        }).listen(8017);
    }
});

server.listen(8017);
console.log('代理服务器运行在 http://localhost:8017');