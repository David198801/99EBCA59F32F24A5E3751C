import gsap from 'gsap';
import {
    Live2DModel,
    MotionPreloadStrategy,
    InternalModel,
} from 'pixi-live2d-display';
import { sleep } from './tools';

export const IDLE_MOTIONS = {
    BLINK:'idle_blink',
    CLOSE_EYES:'idle_close_eyes',
}



export async function loadModel(modelPath, app, x, y,layer): Promise<Live2DModel> {
    const model = await Live2DModel.from(modelPath, {
        motionPreload: MotionPreloadStrategy.ALL,
        autoInteract: false
    });
    app.stage.addChildAt(model,layer);  // 将模型添加到舞台
    model.position.set(x, y);  // 设置模型的位置

    model.scale.set(0.58, 0.58);
    model.anchor.set(0, 0);

    //关闭有问题的自动眨眼
    if (model.internalModel["eyeBlink"]) {
        model.internalModel["eyeBlink"].blinkInterval = 1000 * 60 * 60 * 24;
        model.internalModel["eyeBlink"].nextBlinkTimeLeft = 1000 * 60 * 60 * 24;
    }
    //关闭摇摆
    if (model.internalModel["angleXParamIndex"] !== undefined) model.internalModel["angleXParamIndex"] = 999;
    if (model.internalModel["angleYParamIndex"] !== undefined) model.internalModel["angleYParamIndex"] = 999;
    if (model.internalModel["angleZParamIndex"] !== undefined) model.internalModel["angleZParamIndex"] = 999;

    //关闭呼吸
    // if (model.internalModel["bodyAngleXParamIndex"] !== undefined) model.internalModel["bodyAngleXParamIndex"] = 999;
    // if (model.internalModel["breathParamIndex"] !== undefined) model.internalModel["breathParamIndex"] = 999;


    // model1.internalModel.eyeBlink.setEyeParams(0)

    //默认idle，可指定
    model.internalModel.motionManager.groups.idle = '';

    return model;  // 返回模型对象
}





// 口型同步函数
export async function playVocal(model, path) {
    const state = {
        playing: true,
    };

    const mouth_param_index = model.internalModel.coreModel.getParamIndex("PARAM_MOUTH_OPEN_Y");

    const audioCtx = new AudioContext();

    // 新建分析仪
    const analyser = audioCtx.createAnalyser();

    // 根据 频率分辨率建立个 Uint8Array 数组备用
    const frequencyData = new Uint8Array(analyser.frequencyBinCount);

    // 取音频文件成 arraybuffer
    const request = new XMLHttpRequest();
    request.open('GET', path, true);
    request.responseType = 'arraybuffer';
    request.onload = () => {
        const audioData = request.response;

        audioCtx.decodeAudioData(audioData, function (buffer) {
            // 新建 Buffer 源
            const source = audioCtx.createBufferSource();
            source.buffer = buffer;

            // 连接到 audioCtx
            source.connect(audioCtx.destination);

            // 连接到 音频分析器
            source.connect(analyser);

            // 开始播放
            source.start(0);

            source.onended = () => {
                // 使用外部状态管理
                state.playing = false;
                setMouthOpenY(model, 0)
            };
        });
    };
    request.send();

    // 需要用到频谱的时候 从分析仪获取到 之前备用的 frequencyData 里
    const getByteFrequencyData = () => {
        analyser.getByteFrequencyData(frequencyData);
        return frequencyData;
    };

    const setMouthOpenY = (model, v) => {
        v = Math.max(0, Math.min(1, v));
        model.internalModel.coreModel.setParamFloat(mouth_param_index, v);
    }


    const o = 80;
    const arrayAdd = a => a.reduce((i, a) => i + a, 0);
    const run = () => {
        if (!state.playing) return;
        const frequencyData = getByteFrequencyData();
        const arr = [];
        // 频率范围还是太广了，跳采！
        for (var i = 0; i < 700; i += o) {
            arr.push(frequencyData[i]);
        }
        setMouthOpenY(model, (arrayAdd(arr) / arr.length - 20) / 60 * 0.8);
        setTimeout(run, 1000 / 30);
    }
    run()
}

export async function moveModel(model,x,y,seconds) {
    gsap.to(model.position, {
        x: model.x + x,
        y: model.y + y,
        duration: seconds,
        ease: 'power1.inOut',
        repeat: 0, //0：执行一次，1：重复一次（执行2次），-1是无限循环
        yoyo: false,
    })
}

export async function rotateModel(model, angle, seconds) {
    // 获取模型边界（需确保模型已加载完成）
    const bounds = model.getLocalBounds();

    // 动态补偿偏移：将模型中心对齐到锚点 (0,0) 的等效位置
    gsap.to(model, {
        x: model.x - bounds.width,
        y: model.y + bounds.height,
        rotation: model.rotation + angle,
        duration: seconds,
        ease: 'power1.inOut',
        repeat: 0,
        yoyo: false
    });
}

export async function walk(model,x,y,seconds) {
    const wk = gsap.timeline({repeat: 0});
    const yDuration = 0.25;
    const repeat = Math.floor(seconds/yDuration)-3;
    wk.to(model.position, {
        x: model.x + x,
        duration: seconds,
        ease: 'power1.inOut'
    }).to(model, {
        y: model.y + y + 15,
        duration: yDuration,
        yoyo: true,
        repeat: repeat<0?0:repeat,
        ease: "sine.inOut"
    }, 0);
}



export function stopMotion(model){
    model.internalModel.motionManager.stopAllMotions();
}

export function stopExpression(model){
    model.internalModel.motionManager.expressionManager.stopAllExpressions();
}

export function setIdle(model, value){
    model.internalModel.motionManager.groups.idle = value;
}

export async function openEyes(model, start_value) {
    //coreModel.getParameterValueById(expParamId) 还没试
    model.internalModel.motionManager.groups.idle = '';
    stopExpression(model);

    const left_eye_param_index = model.internalModel.coreModel.getParamIndex("PARAM_EYE_L_OPEN");
    const right_eye_param_index = model.internalModel.coreModel.getParamIndex("PARAM_EYE_R_OPEN");
    

    let currentValue = start_value;
    
    while(1){
        if(currentValue>=1){
            model.internalModel.coreModel.setParamFloat(left_eye_param_index, 1);
            model.internalModel.coreModel.setParamFloat(right_eye_param_index, 1);
            break;
        }else{
            model.internalModel.coreModel.setParamFloat(left_eye_param_index, currentValue);
            model.internalModel.coreModel.setParamFloat(right_eye_param_index, currentValue);
            await sleep(5);
        }
        currentValue += 0.0025;
    }

    setIdle(model, IDLE_MOTIONS.BLINK);
    
}