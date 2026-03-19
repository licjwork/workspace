// 敲木鱼组件测试脚本
const puppeteer = require('puppeteer');

async function testWoodenFish() {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    try {
        console.log('🧪 开始测试敲木鱼组件...');
        
        // 访问页面
        await page.goto('http://localhost:8017');
        console.log('✅ 页面加载成功');
        
        // 检查木鱼元素是否存在
        const fishExists = await page.evaluate(() => {
            return document.getElementById('wooden-fish') !== null;
        });
        console.log(fishExists ? '✅ 木鱼元素存在' : '❌ 木鱼元素不存在');
        
        // 检查计数器
        const initialCount = await page.evaluate(() => {
            const counter = document.getElementById('fish-counter');
            return counter ? parseInt(counter.textContent) : -1;
        });
        console.log(`✅ 初始计数: ${initialCount}`);
        
        // 点击木鱼
        await page.click('#wooden-fish');
        await page.waitForTimeout(500);
        
        // 检查计数是否增加
        const newCount = await page.evaluate(() => {
            const counter = document.getElementById('fish-counter');
            return counter ? parseInt(counter.textContent) : -1;
        });
        console.log(`✅ 点击后计数: ${newCount}`);
        console.log(newCount > initialCount ? '✅ 计数增加成功' : '❌ 计数未增加');
        
        // 检查localStorage
        const localStorageCount = await page.evaluate(() => {
            return parseInt(localStorage.getItem('woodenFishCount')) || 0;
        });
        console.log(`✅ localStorage计数: ${localStorageCount}`);
        console.log(localStorageCount === newCount ? '✅ 本地存储正确' : '❌ 本地存储错误');
        
        console.log('🎉 敲木鱼组件测试完成');
        
    } catch (error) {
        console.error('❌ 测试失败:', error);
    } finally {
        await browser.close();
    }
}

// 运行测试
if (require.main === module) {
    testWoodenFish();
}

module.exports = { testWoodenFish };