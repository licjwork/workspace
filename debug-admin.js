const puppeteer = require('puppeteer');

async function debugAdminPage() {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // 监听控制台错误
    page.on('console', msg => {
        console.log('浏览器控制台:', msg.type(), msg.text());
    });
    
    page.on('error', err => {
        console.log('页面错误:', err);
    });
    
    try {
        console.log('正在访问后台管理页面...');
        await page.goto('http://82.156.52.192:8017/admin/', { waitUntil: 'networkidle0' });
        
        // 检查页面内容
        const title = await page.title();
        console.log('页面标题:', title);
        
        // 检查是否显示登录界面
        const loginVisible = await page.$eval('#login-container', el => {
            return window.getComputedStyle(el).display !== 'none';
        });
        console.log('登录界面是否可见:', loginVisible);
        
        // 检查管理界面
        const adminVisible = await page.$eval('#admin-container', el => {
            return window.getComputedStyle(el).display !== 'none';
        });
        console.log('管理界面是否可见:', adminVisible);
        
        // 截图
        await page.screenshot({ path: '/home/ubuntu/.openclaw/workspace/admin-screenshot.png' });
        console.log('截图已保存');
        
    } catch (error) {
        console.error('调试出错:', error);
    } finally {
        await browser.close();
    }
}

debugAdminPage();