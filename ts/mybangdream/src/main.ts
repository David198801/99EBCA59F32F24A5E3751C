import * as PIXI from 'pixi.js'
import {
  Live2DModel,
  MotionPreloadStrategy,
  InternalModel,
} from 'pixi-live2d-display';

// 挂载pixi
window.PIXI = PIXI;
(async function () {

  const app = await init(1920,1080);

  

  // // 引入模型
  const model1 = await loadModel({
    app:app,
    modelPath:'../res/live2d/001_casual_summer-2023/model.json',
    x:100,
    y:0
  })


  const model2 = await loadModel({
    app:app,
    modelPath:'../res/live2d/001_casual_summer-2023/model.json',
    x:800,
    y:0
  })


})();


async function init(w,h) {
  const canvas_view = document.getElementById('canvas_view') as HTMLCanvasElement;

  const app = new PIXI.Application({
    view: canvas_view,
    // 背景是否透明
    transparent: true,
    autoDensity:true,
    antialias: true,
    width: w,
    height: h
  });

  canvas_view.style.border = '2px solid black';

  scaleCanvas(app, canvas_view);

  return app;
}

async function loadModel(params): Promise<Live2DModel> {
  let model = await Live2DModel.from(params.modelPath, {
    motionPreload: MotionPreloadStrategy.ALL,
    autoInteract: false
  });
  params.app.stage.addChild(model);  // 将模型添加到舞台
  model.position.set(params.x, params.y);  // 设置模型的位置

  model.scale.set(0.5, 0.5);
  model.anchor.set(0, 0);
  
  return model;  // 返回模型对象
}

// 确保画布等比例缩小
function scaleCanvas(app, canvas_view) {
  const screenWidth = document.documentElement.clientWidth;
  const scaleFactor = 0.8; // 设置canvas宽度为屏幕宽度的80%
  const newWidth = screenWidth * scaleFactor;

  // 计算新的高度以保持宽高比例
  const aspectRatio = app.view.width / app.view.height;
  const newHeight = newWidth / aspectRatio;

  // 设置canvas的显示大小
  canvas_view.style.width = newWidth + 'px';
  canvas_view.style.height = newHeight + 'px';
}

const fullscreenButton = document.getElementById('fullscreen_button');
// 全屏按钮点击事件
fullscreenButton.addEventListener('click', () => {
  const canvas_view = document.getElementById('canvas_view') as HTMLCanvasElement;
  if (canvas_view.requestFullscreen) {
    canvas_view.requestFullscreen();
  }
});

