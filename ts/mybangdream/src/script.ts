import { changeBg, clearApp, drawMenu, drawName, drawNameAndText, drawText, drawAuto, LAYER, startIn, drawNameBoxAndTextBoxStartIn, turnIn, end, hideBlack, drawNameBoxAndTextBoxTurnIn } from "./draw";
import { loadModel, playVocal, moveModel, walk, stopMotion, openEyes, IDLE_MOTIONS, stopExpression, setIdle, rotateModel, setModelAlpha } from "./live2d";
import { playAudio, sleep } from "./tools";
import type { Live2DModel, InternalModel } from "pixi-live2d-display";

export async function play(app, isFullScreen: boolean) {

    //初始化加载
    await clearApp(app);
    drawMenu(app);
    await changeBg(app, "../res/background/t1.jpg");//背景

    // 全屏录制时等待6秒
    if (isFullScreen) {
        await sleep(6 * 1000);
    }

    await startIn(app,"花咲川女子学园 校门前");
    
    const ako = await loadModel('../res/live2d/024_casual_summer-2023/model.json', app, 50, -80, LAYER.LIVE2D1);
    const rinrin = await loadModel('../res/live2d/025_casual_summer-2023/model.json', app, 620, -80, LAYER.LIVE2D2);
    //模型同步显示
    await setModelAlpha([ako,rinrin], 1);
    //弹出对话框
    await drawNameBoxAndTextBoxStartIn(app);
    await drawAuto(app);

    rinrin.expression("smile01");
    ako.expression("smile01");
    drawName(app, "亚子");

    //model.internalModel.motionManager.groups.idle = 'idle_blink';

    /*
    睁眼
    stopMotion(anon);
    playVocal(anon,"../res/vocal/17_密码我早偷就看到了。a，n，s，y_2.wav");
    
    openEyes(anon, 0.6);
    anon.motion("smile01")
    anon.expression("smile01");
    */
    
    //moveModel(model1,300,0,1)
    //playAudio("../res/vocal/08_.wav");
    //walk(model1,1000,0,3);
    //rotateModel(ksm,-1.5,2);
    //rotateModel(ako,20 * Math.PI/180,2);

    drawNameAndText(app, "亚子", "今天玩得真尽兴啊！");
    playVocal(ako,"../res/vocal/13_今天玩得真尽兴啊！.wav");
    ako.motion("smile06");
    ako.expression("ako_special02");

    await sleep(2.5 * 1000);
    console.log(2);console.log(app.stage.children.length)
    stopMotion(ako);
    ako.expression("smile01");
    await sleep(1 * 1000);

    

    //结束：缩小对话框+黑屏,
    // 传入下一次对话框初始名称
    // 黑屏时操作传入函数处理
    await end(app, "亚子", function(){
        //切换背景
        changeBg(app, "../res/background/bg00046 燐子家 1080.png");
        //隐藏模型
        setModelAlpha([ako,rinrin], 0);
        //换位置、载入新模型等
        ako.x = 620;
        rinrin.x = 50; 
    });


    //黑屏转场out
    await hideBlack(app);
    //转场条
    await turnIn(app,"白金家 燐子房间");
    //模型同步显示
    await setModelAlpha([ako,rinrin], 1);
    //弹出对话框
    await drawNameBoxAndTextBoxTurnIn(app);
    await drawAuto(app);

    drawNameAndText(app, "亚子", "但是感觉有些浪费呢，颜料都粘在一起了");
    playVocal(ako,"../res/vocal/14_但是感觉有些浪费呢，颜料都粘在一起了.wav");
    ako.motion("serious01");
    

    await sleep(6 * 1000);

    drawNameAndText(app, "燐子", "是可食用颜料哦，等会吃掉就好了");
    playVocal(rinrin,"../res/vocal/15_是可食用颜料哦，等会吃掉就好了2.wav");
    rinrin.motion("smile03");
    rinrin.expression("smile03");

    await sleep(7.5 * 1000);
    
}