import { changeBg, clearApp, drawName, drawNameAndText, drawText, drawUI, LAYER } from "./draw";
import { loadModel, playVocal, moveModel, walk, stopMotion, openEyes, IDLE_MOTIONS, stopExpression, setIdle, rotateModel } from "./live2d";
import { playAudio, sleep } from "./tools";
import type { Live2DModel, InternalModel } from "pixi-live2d-display";

export async function play(app, isFullScreen: boolean) {

    //初始化加载
    clearApp(app);
    await changeBg(app, "../res/background/bg00039 仓库 43 1080.png");//背景
    const ksm = await loadModel('../res/live2d/001_school_summer-2023/model.json', app, 100, -85, LAYER.LIVE2D2);
    const ars = await loadModel('../res/live2d/005_pajamas-2023/model.json', app, 620, 220, LAYER.LIVE2D2);
    await drawUI(app);
    ars.expression("shame01");
    ksm.expression("sad01");
    drawName(app, "香澄");
    

/**/
    // 等待6秒
    if (isFullScreen) {
        await sleep(6 * 1000);
    }

    playAudio("../res/vocal/刮毛.wav");

    drawNameAndText(app, "香澄", "还没好吗？还没好嘛？");
    playVocal(ksm,"../res/vocal/01_还没好吗？还没好嘛？2.wav");
    ksm.motion("nnf02");
    ksm.expression("sad01");

    await sleep(3 * 1000);

    drawNameAndText(app, "有咲", "不要乱动啊！剃须膏都沾到沙发上了！");
    playVocal(ars,"../res/vocal/02_不要乱动啊！剃须膏都沾到沙发上了2.wav");
    ars.motion("angry03");

    await sleep(6 * 1000);

    drawNameAndText(app, "香澄", "有点怕怕~");
    playVocal(ksm,"../res/vocal/03_感觉怕怕~.wav");
    ksm.motion("sad01");
    ksm.expression("sad01");
   
    await sleep(4 * 1000);

    drawNameAndText(app, "有咲", "有什么好怕的？你以为我修剪过多少盆栽了啊？");
    playVocal(ars,"../res/vocal/04_有啥好怕的？你以为我修剪过多少盆栽了啊？2.wav");
    ars.motion("angry01");

    await sleep(6 * 1000);

    playAudio("../res/vocal/剪刀.wav");

    await sleep(2.5 * 1000);

    drawNameAndText(app, "有咲", "好了，星星的形状完成了");
    playVocal(ars,"../res/vocal/06_好了，星星的形状完成了.wav");
    ars.motion("kime01");
    ars.expression("smile01");

    moveModel(ars,0,-300,2);

    await sleep(3.5 * 1000);

    drawNameAndText(app, "香澄", "哇，闪闪发光！");
    playVocal(ksm,"../res/vocal/07_哇，闪闪发光！.wav");
    ksm.motion("smile04");
    ksm.expression("smile01");

    await sleep(3.5 * 1000);

    drawNameAndText(app, "有咲", "接下来签个名吧");
    playVocal(ars,"../res/vocal/08_接下来签个名吧.wav");
    ars.motion("bye01");
    ars.expression("smile01");

    await sleep(3 * 1000);
    drawNameAndText(app, "香澄", "……");
    await sleep(2.5 * 1000);

    drawNameAndText(app, "有咲", "喂，给点反应啊！");
    playVocal(ars,"../res/vocal/10_喂，给点反应啊！.wav");
    ars.motion("nf02");
    ars.expression("idle01");

    await sleep(3 * 1000);

    drawNameAndText(app, "香澄", "我觉得有咲的话签个名也是可以接受的");
    playVocal(ksm,"../res/vocal/11_我觉得有咲的话签个名也是可以接受的2.wav");
    ksm.motion("smile01");
    ksm.expression("smile01");

    await sleep(4 * 1000);

    drawNameAndText(app, "有咲", "你傻吗？当然是开玩笑的！");
    playVocal(ars,"../res/vocal/12_你傻吗？当然是开玩笑的！.wav");
    ars.motion("angry03");
    ars.expression("shame01");

    await sleep(6 * 1000);

    drawNameAndText(app, "有咲", "那个，香澄……给我看看星之鼓动吧……");
    playVocal(ars,"../res/vocal/13_那个，香澄 15_给我看看星之鼓动吧…….wav");
    ars.motion("shame01");
    ars.expression("shame01");

    await sleep(5 * 1000);

    drawNameAndText(app, "香澄", "来吧来吧！今天弹《野蜂飞舞》我都不怕了！");
    playVocal(ksm,"../res/vocal/16_来吧来吧！今天弹《野蜂飞舞》我都不怕了！.wav");
    ksm.motion("kime01");
    ksm.expression("smile01");

    await sleep(4 * 1000);

    rotateModel(ksm,-1.5,2);

    await sleep(2 * 1000);

    drawNameAndText(app, "有咲", "《小星星》都受不了还吹牛呢……");
    playVocal(ars,"../res/vocal/17_《小星星》都受不了还吹牛呢…….wav");
    ars.motion("smile01");
    ars.expression("smile01");

    await sleep(3 * 1000);

    rotateModel(ars,-1.5,2);





}