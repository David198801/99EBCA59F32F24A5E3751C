import { changeBg, clearApp, drawName, drawNameAndText, drawText, drawUI, LAYER } from "./draw";
import { loadModel, playVocal, moveModel, walk, stopMotion, openEyes, IDLE_MOTIONS, stopExpression, setIdle, rotateModel } from "./live2d";
import { playAudio, sleep } from "./tools";
import type { Live2DModel, InternalModel } from "pixi-live2d-display";

export async function play(app, isFullScreen: boolean) {

    //初始化加载
    clearApp(app);
    await changeBg(app, "../res/background/bg00046 燐子家 1080.png");//背景
    const ako = await loadModel('../res/live2d/024_casual_summer-2023/model.json', app, -900, -80, LAYER.LIVE2D2);
    const rinrin = await loadModel('../res/live2d/025_casual_summer-2023/model.json', app, 620, -80, LAYER.LIVE2D2);
    await drawUI(app);
    rinrin.expression("default");
    ako.expression("default");
    drawName(app, "燐子");
    


    // 等待6秒
    if (isFullScreen) {
        await sleep(6 * 1000);
    }

    drawNameAndText(app, "燐子", "可以进来了");
    playVocal(rinrin,"../res/vocal/01_可以进来了2.wav");
    rinrin.motion("idle01");

    await sleep(3 * 1000);

    drawNameAndText(app, "亚子", "来了！");
    playVocal(ako,"../res/vocal/02_来了！.mp3");
    ako.motion("smile06");
    ako.expression("smile02");

    moveModel(ako,950,0,2);

    stopMotion(rinrin);
    await sleep(3 * 1000);

    drawNameAndText(app, "燐子", "请看吧……我的魔纹……");
    playVocal(rinrin,"../res/vocal/03_请看吧……我的魔纹…….wav");
    rinrin.motion("mite");

    await sleep(4 * 1000);

    drawNameAndText(app, "亚子", "唉？原来是在这个地方么？");
    playVocal(ako,"../res/vocal/04_唉？原来是在这个地方么？.wav");
    ako.motion("surprised01");
    ako.expression("surprised01");

    await sleep(2.5 * 1000);
    stopMotion(ako);
    await sleep(1 * 1000);

    drawNameAndText(app, "亚子", "但是为什么燐燐会有呢？难道燐燐其实是梦魔？");
    playVocal(ako,"../res/vocal/05_但是为什么燐燐会有呢？难道燐燐其实是梦魔？2.wav");
    ako.motion("eeto01");

    await sleep(4 * 1000);
    stopMotion(ako);
    ako.motion("gattsu02");
    await sleep(3.5 * 1000);

    drawNameAndText(app, "燐子", "因为……小亚子说想了解……我就自己画了一个");
    playVocal(rinrin,"../res/vocal/06_因为……小亚子说想了解……我就自己画了一个.wav");
    rinrin.motion("smile01");
    rinrin.expression("smile01");

    await sleep(5 * 1000);
    stopMotion(rinrin);
    await sleep(2 * 1000);
    stopExpression(rinrin);
    

    drawNameAndText(app, "燐子", "那个……小亚子你一直盯着我的话……我……");
    playVocal(rinrin,"../res/vocal/07_那个……小亚子你一直盯着我的话……我…….wav");
    rinrin.expression("rinko_shame");
    rinrin.motion("shame01");

    await sleep(6 * 1000);

    drawNameAndText(app, "亚子", "啊，对不起，我去拿纸巾");
    playVocal(ako,"../res/vocal/08_啊，对不起，我去拿纸巾.wav");
    ako.motion("surprised01");
    ako.expression("serious01");

    await sleep(1 * 1000);
    moveModel(ako,-400,0,1);
    await sleep(2 * 1000);
    stopMotion(ako);
    moveModel(ako,400,0,1);
    await sleep(1.5 * 1000);
    stopExpression(ako);

    drawNameAndText(app, "亚子", "燐燐你没事吧，看你冷得瑟瑟发抖");
    playVocal(ako,"../res/vocal/09_燐燐你没事吧，看你冷得瑟瑟发抖.wav");
    ako.motion("nnf02");
    ako.expression("sad01");

    await sleep(4 * 1000);

    drawNameAndText(app, "燐子", "没事……是空调……开得太低了");
    playVocal(rinrin,"../res/vocal/10_1没事……是空调……开得太低了.wav");
    rinrin.motion("nf_right01");
    rinrin.expression("smile01");
    
    await sleep(5.5 * 1000);

    drawNameAndText(app, "亚子", "那就好，吓死我了");
    playVocal(ako,"../res/vocal/10_2那就好，吓死我了2.wav");
    ako.motion("smile05");
    ako.expression("smile03");

    await sleep(3 * 1000);

    playAudio("../res/vocal/空调.wav");

    await sleep(2.5 * 1000);

    drawNameAndText(app, "燐子", "要不要……给小亚子也画一个？");
    playVocal(rinrin,"../res/vocal/11_要不要……给小亚子也画一个？.wav");
    rinrin.motion("smile01");
    rinrin.expression("smile01");

    await sleep(4 * 1000);

    drawNameAndText(app, "亚子", "好啊，我们来对战吧！");
    playVocal(ako,"../res/vocal/12_好啊，我们来对战吧！.wav");
    ako.motion("nnf05");
    ako.expression("ako_special02");
}