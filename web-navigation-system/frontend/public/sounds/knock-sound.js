// 真实木鱼音效生成器
class KnockSound {
    constructor() {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    // 生成真实的"咚"声音效
    playKnockSound() {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        // 木鱼音效参数
        oscillator.frequency.value = 220; // A3音符，更接近木鱼声音
        oscillator.type = 'sine';
        
        // 快速衰减的包络
        gainNode.gain.setValueAtTime(0.5, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.5);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.5);
    }

    // 生成多个频率的音效，模拟真实木鱼
    playRealKnock() {
        const now = this.audioContext.currentTime;
        
        // 主音
        const mainOsc = this.audioContext.createOscillator();
        const mainGain = this.audioContext.createGain();
        mainOsc.connect(mainGain);
        mainGain.connect(this.audioContext.destination);
        
        mainOsc.frequency.value = 220;
        mainOsc.type = 'sine';
        mainGain.gain.setValueAtTime(0.4, now);
        mainGain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
        
        // 泛音
        const harmonicOsc = this.audioContext.createOscillator();
        const harmonicGain = this.audioContext.createGain();
        harmonicOsc.connect(harmonicGain);
        harmonicGain.connect(this.audioContext.destination);
        
        harmonicOsc.frequency.value = 440;
        harmonicOsc.type = 'sine';
        harmonicGain.gain.setValueAtTime(0.2, now);
        harmonicGain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        
        mainOsc.start(now);
        harmonicOsc.start(now);
        mainOsc.stop(now + 0.6);
        harmonicOsc.stop(now + 0.4);
    }
}

window.KnockSound = KnockSound;