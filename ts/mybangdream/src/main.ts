import * as PIXI from 'pixi.js'
import {
  Live2DModel,
  MotionPreloadStrategy,
  InternalModel,
} from 'pixi-live2d-display';

// 挂载pixi
window.PIXI = PIXI;

export async function init() {
  // 引入模型
const model = await Live2DModel.from('../../src/assets/model2/HK416_805/normal.model3.json', { motionPreload: MotionPreloadStrategy.NONE,  })


// 创建模型对象
const app = new PIXI.Application({
  // 配置模型舞台
  view: document.getElementById('canvas_view') as HTMLCanvasElement,
  // 背景是否透明
  transparent: true,
  autoDensity:true,
  antialias: true,
  // 高度
  height: 1080,
  // 宽度
  width:1900
})
}
