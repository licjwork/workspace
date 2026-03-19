// 敲木鱼小组件
class WoodenFish {
    constructor() {
        this.count = parseInt(localStorage.getItem('woodenFishCount')) || 0;
        this.isPlaying = false;
        this.init();
    }

    init() {
        // 创建木鱼元素
        this.createWoodenFishElement();
        // 预加载音效
        this.loadSound();
        // 绑定事件
        this.bindEvents();
    }

    createWoodenFishElement() {
        const fishHtml = `
            <div id="wooden-fish-container" class="wooden-fish-container">
                <div class="wooden-fish" id="wooden-fish">
                    <div class="fish-icon">🐟</div>
                    <div class="fish-counter" id="fish-counter">${this.count}</div>
                </div>
                <div class="fish-tooltip">敲木鱼</div>
            </div>
        `;
        
        // 添加到页面
        document.body.insertAdjacentHTML('beforeend', fishHtml);
        
        this.fishElement = document.getElementById('wooden-fish');
        this.counterElement = document.getElementById('fish-counter');
    }

    loadSound() {
        // 使用Web Audio API生成木鱼音效
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    playSound() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 440; // A4音符
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.3);
    }

    knock() {
        if (this.isPlaying) return;
        
        this.isPlaying = true;
        this.count++;
        
        // 播放音效
        this.playSound();
        
        // 更新计数器
        this.counterElement.textContent = this.count;
        
        // 添加敲击动画
        this.fishElement.classList.add('knocking');
        setTimeout(() => {
            this.fishElement.classList.remove('knocking');
            this.isPlaying = false;
        }, 300);
        
        // 保存到本地存储
        localStorage.setItem('woodenFishCount', this.count.toString());
        
        console.log(`敲木鱼 ${this.count} 次`);
    }

    bindEvents() {
        const fishElement = document.getElementById('wooden-fish');
        
        // 鼠标点击事件
        fishElement.addEventListener('click', () => {
            this.knock();
        });
        
        // 触摸事件（移动端）
        fishElement.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.knock();
        });
        
        // 键盘快捷键（空格键）
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.knock();
            }
        });
    }

    reset() {
        this.count = 0;
        this.counterElement.textContent = this.count;
        localStorage.setItem('woodenFishCount', '0');
    }

    getCount() {
        return this.count;
    }
}

// 初始化木鱼组件
window.WoodenFish = WoodenFish;