import { changeBg, clearApp, drawName, drawNameAndText, drawText, drawUI } from "./draw";
import { loadModel, playVocal, moveModel, walk } from "./live2d";
import { playAudio, sleep } from "./tools";
import type { Live2DModel, InternalModel } from "pixi-live2d-display";

export async function play(app, isFullScreen: boolean) {

    //初始化加载
    clearApp(app);
    await changeBg(app, "../res/background/b1 01 明日香房间AI_waifu2x_2x_png (2).png");//背景
    const model2 = await loadModel('../res/live2d/214_school_winter-2023_sleep/model.json', app, 720, -80);
    model2.internalModel.motionManager.groups.idle = 'idle_close_eyes';//闭眼
    const model1 = await loadModel('../res/live2d/001_casual_summer-2023/model.json', app, 50, -82);
    await drawUI(app);
    drawName(app,"香澄")

    





}