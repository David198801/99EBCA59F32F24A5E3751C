import { changeBg, clearApp, drawName, drawNameAndText, drawText, drawUI } from "./draw";
import { loadModel, playVocal, moveModel } from "./live2d";
import { sleep } from "./tools";
import type { Live2DModel, InternalModel } from "pixi-live2d-display";

export async function play(app, isFullScreen: boolean) {

    //初始化加载
    clearApp(app);
    await changeBg(app, "../devres/img/bg00363_1080.png");//背景
    const model1 = await loadModel('../devres/live2d/001_casual_summer-2023/model.json', app, 50, -80);
    //const model2 = await loadModel('../devres/live2d/001_casual_summer-2023/model.json', app, 720, -80);
    await drawUI(app);
    //drawName(app,"沙绫")

    


    // 等待6秒
    if (isFullScreen) {
        await sleep(6 * 1000);
    }

    //drawText(app,"你的我的深刻的发涩发色粉是否色是否色法色法\n手动阀手动阀的是粉色粉色发身公爵大人果然粉色")
    drawNameAndText(app, "沙绫", "你的我的深刻的发涩发色粉是否色是否色法色法\n手动阀手动阀的是粉色粉色发身公爵大人果然粉色")
    playVocal(model1,"../devres/audio/5BPS-loginstory-028_あの～、せっかくの機会だからひとつ提案があるんですけど…….mp3");

    
   
    
    model1.motion("hukumi01");
    model1.expression("smile01");
    await sleep(7 * 1000);

    //model1.x += 100;
    moveModel(model1,300,0,1)

    //playAudio("../res/volcal/08_.wav");
    //walk(model1,1000,0,3);
    
    model1.motion("nf02");









}

function playAudio(arg0: string) {
    throw new Error("Function not implemented.");
}
function walk(model1: Live2DModel<InternalModel>, arg1: number, arg2: number, arg3: number) {
    throw new Error("Function not implemented.");
}

