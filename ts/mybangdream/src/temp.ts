const unmuteButton = document.getElementById("unmuteButton");
// 为按钮添加点击事件监听器
unmuteButton.addEventListener("click", () => {
  // 获取audio元素和按钮
  const audio = document.getElementById("audio") as HTMLAudioElement;
  audio.muted = false; // 取消静音
});

function playSound(path){
  // 获取audio元素和按钮
  const audio = document.getElementById("audio") as HTMLAudioElement;
  audio.src=path;
  audio.play();
}