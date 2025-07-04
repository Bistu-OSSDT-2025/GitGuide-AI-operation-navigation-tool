document.getElementById("execute").addEventListener("click", () => {
  const command = document.getElementById("command").value.trim();

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: jumpToSection,
      args: [command]
    });
  });
});

function jumpToSection(command) {
  const navMap = {
    "首页": "首页",
    "环保活动": "环保活动",
    "减碳小贴士": "减碳小贴士",
    "环保留言板": "环保留言板",
    "概述": "overview",
    "中轴线地图": "map",
    "地标建筑": "landmarks",
    "现代建筑": "modern"
  };

  const landmarkIds = [
    "永定门", "先农坛", "天坛", "正阳门", "天安门广场", "天安门",
    "外金水桥", "端门", "故宫", "太庙", "社稷坛", "景山",
    "万宁桥", "钟鼓楼", "鸟巢", "水立方"
  ];

  let found = false;

  // 导航点击逻辑（寻找链接）
  for (const key in navMap) {
    if (command.includes(key)) {
      const links = document.querySelectorAll("a");
      for (const link of links) {
        if (link.textContent.includes(navMap[key])) {
          link.click();
          alert(`已点击跳转到：${key}`);
          found = true;
          return;
        }
      }
    }
  }

  // 滚动到主板块或地标
  const allTargets = { ...navMap };
  landmarkIds.forEach(id => { allTargets[id] = id; });

  for (const key in allTargets) {
    if (command.includes(key)) {
      const el = document.getElementById(allTargets[key]);
      if (el) {
        el.scrollIntoView({ behavior: "smooth" });
        alert(`已滚动到：${key}`);
        found = true;
        return;
      }
    }
  }

  if (!found) {
    alert("未识别指令，请尝试：跳转到天坛、概述等。");
  }
}
