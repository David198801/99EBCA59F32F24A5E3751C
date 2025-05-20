import { init } from './draw';
import { play } from './script';

(async function () {

  const app = await init(1920, 1080);

  const paly_button = document.getElementById('paly_button');
  paly_button.addEventListener('click', () => {
    play(app, false);
  });


  const fullscreenButton = document.getElementById('fullscreen_button');
  // 全屏按钮点击事件
  fullscreenButton.addEventListener('click', () => {
    const canvas_view = document.getElementById('canvas_view') as HTMLCanvasElement;
    if (canvas_view.requestFullscreen) {
      canvas_view.requestFullscreen();
    }
    play(app, true);
  });

})();










