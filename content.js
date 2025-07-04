// 监听页面加载完成事件
document.addEventListener('DOMContentLoaded', function() {
    // 为所有地标添加高亮效果
    highlightLandmarks();
    
    // 添加跳转动画效果
    addScrollAnimations();
    
    // 增强导航功能
    enhanceNavigation();
});

function highlightLandmarks() {
    const landmarks = [
        "永定门", "先农坛", "天坛", "正阳门", "天安门广场", "天安门",
        "外金水桥", "端门", "故宫", "太庙", "社稷坛", "景山",
        "万宁桥", "钟鼓楼", "鸟巢", "水立方"
    ];
    
    landmarks.forEach(landmark => {
        const element = document.getElementById(landmark);
        if (element) {
            element.classList.add('landmark-highlight');
            
            // 添加点击事件，方便用户交互
            element.addEventListener('click', function() {
                this.classList.toggle('landmark-active');
            });
        }
    });
}

function addScrollAnimations() {
    // 观察器用于动画触发
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, { threshold: 0.1 });
    
    // 观察所有章节和地标
    document.querySelectorAll('section, .landmark').forEach(section => {
        observer.observe(section);
        section.classList.add('animate-ready');
    });
}

function enhanceNavigation() {
    // 为导航链接添加平滑滚动
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                    
                    // 更新URL而不重新加载页面
                    history.pushState(null, null, href);
                }
            }
        });
    });
    
    // 处理页面加载时的锚点
    if (window.location.hash) {
        setTimeout(() => {
            const target = document.querySelector(window.location.hash);
            if (target) {
                target.scrollIntoView();
            }
        }, 100);
    }
}

// 暴露一些函数给popup.js使用
window.jumpToSection = function(command) {
    // 这里可以添加更多自定义跳转逻辑
    const element = document.getElementById(command);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth'
        });
        
        // 添加临时高亮
        element.classList.add('temp-highlight');
        setTimeout(() => {
            element.classList.remove('temp-highlight');
        }, 2000);
        
        return true;
    }
    return false;
};