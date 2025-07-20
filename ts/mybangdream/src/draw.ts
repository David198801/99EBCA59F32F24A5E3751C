import * as PIXI from 'pixi.js'
import { sleep } from './tools';
import gsap from 'gsap';
import { remove } from 'pixi-live2d-display';
import { setModelAlpha } from './live2d';

window.PIXI = PIXI;

export const LAYER = {
    BG : 0,
    LIVE2D1 : 1,
    LIVE2D2 : 2,
    LIVE2D3 : 3,
    LIVE2D4 : 4,
    LIVE2D5 : 5,
    UI1 : 6,
    UI2 : 7,
    UI3 : 8,
    UI4 : 9,
    UI5 : 10,
    UI6 : 11,
    UI7 : 12,
    UI8 : 13,
    UI9 : 14,
    UI10 : 15,
    UI11 : 16,
    UI12 : 17,
    BLACK : 18,
}


export async function init(w, h) {
    const canvas_view = document.getElementById('canvas_view') as HTMLCanvasElement;

    const app = new PIXI.Application({
        view: canvas_view,
        // 背景是否透明
        transparent: true,
        autoDensity: true,
        antialias: true,
        width: w,
        height: h
    });

    canvas_view.style.border = '2px solid black';

    scaleCanvas(app, canvas_view);
    return app;
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


// 新增的changeBg函数
export async function changeBg(app, imageUrl) {
    // 创建一个新的Sprite来显示背景图片
    const background = PIXI.Sprite.from(imageUrl);

    // 设置背景图片的大小为整个画布
    background.width = app.screen.width;
    background.height = app.screen.height;


    app.stage.removeChildAt(LAYER.BG);
    app.stage.addChildAt(background,LAYER.BG);
}

const IntervalIds = {
    autoIntervalId: null
}

export async function drawMenu(app) {
    const menu = PIXI.Sprite.from("../res/img/右上角菜单.png");
    menu.width = app.screen.width;
    menu.height = app.screen.height;
    app.stage.removeChildAt(LAYER.UI10);
    app.stage.addChildAt(menu, LAYER.UI10);
}

export async function drawAuto(app) {
    const auto = PIXI.Sprite.from("../res/img/AUTO.png");
    auto.x = 1510;  // 设置X坐标
    auto.y = 785;  // 设置Y坐标
    auto.width = 150;
    auto.height = 50;
    app.stage.removeChildAt(LAYER.UI3);
    app.stage.addChildAt(auto, LAYER.UI3);
    // 让uiLayer每500毫秒闪烁
    if (IntervalIds.autoIntervalId) {
        console.log("claerInterval:" + IntervalIds.autoIntervalId)
        clearInterval(IntervalIds.autoIntervalId); // 如果有上一个interval，先清除
    }
    let isVisible = true;
    IntervalIds.autoIntervalId = setInterval(() => {
        auto.visible = isVisible;
        isVisible = !isVisible;  // 切换可见性
    }, 500);
}

export async function drawNameBox(app) {
    
    const nameBox = PIXI.Sprite.from("../res/img/姓名框.png");
    nameBox.width = app.screen.width;
    nameBox.height = app.screen.height;

    app.stage.removeChildAt(LAYER.UI2);
    app.stage.addChildAt(nameBox, LAYER.UI2);
}

export async function drawTextBox(app) {
    

    const duration = 0.1;

    await sleep(duration * 1000);
    
    const textBox = PIXI.Sprite.from("../res/img/对话框.png");
    textBox.width = app.screen.width * 0.35;
    textBox.height = app.screen.height  *  0.35;
    textBox.x = 625;
    textBox.y = 595;
    app.stage.removeChildAt(LAYER.UI1);
    app.stage.addChildAt(textBox, LAYER.UI1);


    gsap.to(textBox, {
        width: app.screen.width * 1.1,  // 目标宽度
        height: app.screen.height * 1.1, // 目标高度
        x: -95,                         // 目标X坐标
        y: -90,                         // 目标Y坐标
        duration: duration,                  // 100毫秒时长
        ease: "power1.inOut"            // 平滑缓动效果[6](@ref)
    });

    await sleep(duration * 1000);

    gsap.to(textBox, {
        width: app.screen.width,  // 目标宽度
        height: app.screen.height, // 目标高度
        x: 0,                         // 目标X坐标
        y: 0,                         // 目标Y坐标
        duration: duration,                  // 100毫秒时长
        ease: "power1.inOut"            // 平滑缓动效果[6](@ref)
    });

    await sleep(duration * 1000);
}

export async function drawNameBoxAndTextBox(app) {
    await drawTextBox(app);
    await drawNameBox(app);
}

export async function clearApp(app) {
    app.stage.removeChildren().forEach(child => child.destroy());

    //预先填充图层
    const layerNum = Object.keys(LAYER).length;
    for (let i = 0; i < layerNum; i++) {
        const placeholder = new PIXI.Container();
        placeholder.visible = false; // 可选：隐藏占位元素
        app.stage.addChildAt(placeholder, i);
    }
}


export function drawNameAndText(app, name, text) {
    drawName(app, name);
    drawText(app, text);
}

export function drawName(app, textContent) {
    const text = new PIXI.Text(textContent, {
        fontFamily: "方正兰亭圆_GBK_中",  // 设置字体
        fontSize: 45,      // 设置字体大小
        fill: "#FFFCFF",     // 设置字体颜色（16进制RGB）#515050
    });

    // 设置文本位置
    text.x = 225;  // X坐标
    text.y = 750;  // Y坐标

    // 将文本添加到舞台
    app.stage.removeChildAt(LAYER.UI4);
    app.stage.addChildAt(text,LAYER.UI4);

}


export function drawText(app, textContent) {
    const text = new PIXI.Text("", {
        fontFamily: "方正兰亭圆_GBK_中",  // 设置字体
        fontSize: 40,      // 设置字体大小
        fill: "#515050",     // 设置字体颜色（16进制RGB）
    });

    // 设置文本位置
    text.x = 235;  // X坐标
    text.y = 830;  // Y坐标

    // 将文本添加到舞台
    app.stage.removeChildAt(LAYER.UI5);
    app.stage.addChildAt(text,LAYER.UI5);


    //打字机效果
    let currentIndex = 0;
    const interval = setInterval(() => {
        text.text += textContent[currentIndex];
        currentIndex++;

        // 当所有字符都显示完时，清除定时器
        if (currentIndex === textContent.length) {
            clearInterval(interval);
        }
    }, 100);  // 每100毫秒打出一个字符
}


// 开场
export async function startIn(app, textContent) {
    const duration = 0.6;
    const showTime = 1.1;


    //红条
    const red = PIXI.Sprite.from("../res/img/红条.png");
    red.width = app.screen.width;
    red.height = app.screen.height;
    app.stage.removeChildAt(LAYER.UI6);
    app.stage.addChildAt(red, LAYER.UI6);

    //白条
    const white = PIXI.Sprite.from("../res/img/白条.png");
    white.width = app.screen.width;
    white.height = app.screen.height;
    app.stage.removeChildAt(LAYER.UI7);
    app.stage.addChildAt(white, LAYER.UI7);

    //文本
    const text = new PIXI.Text("", {
        fontFamily: "方正兰亭圆_GBK_中",  // 设置字体
        fontSize: 40,      // 设置字体大小
        fill: "#515050",     // 设置字体颜色（16进制RGB）
    });
    // 关键步骤：设置锚点为中心
    text.anchor.set(0.5); // 中心对齐
    // 初始居中
    text.x = app.screen.width / 2;
    text.y = app.screen.height / 2;
    text.text = textContent;
    app.stage.removeChildAt(LAYER.UI8);
    app.stage.addChildAt(text,LAYER.UI8);

    //显示1秒
    await sleep(showTime * 1000);


    // 创建 GSAP 时间线（控制动画序列）
    const timeline = gsap.timeline();
    // 红条动画（500ms）
    timeline.to(red, {
        x: red.x - 230,
        y: red.x - 50,
        rotation: red.rotation + 3 * Math.PI/180,
        alpha: 0,
        duration: duration,          
        ease: "power1.inOut" 
    }, 0);
    // 白条动画（与红条同时开始）
    timeline.to(white, {
        x: white.x - 230,                 
        alpha: 0,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);        
    // 文字动画
    timeline.to(text, {
        x: text.x - 230,                 
        alpha: 0,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);         
    
    await sleep(duration * 1000 + 100);
}

// 转场，也可用于开场
export async function turnIn(app, textContent) {
    console.log(textContent)
    const duration = 0.6;
    const showTime = 1.1;

    //红条
    const red = PIXI.Sprite.from("../res/img/红条.png");
    red.width = app.screen.width;
    red.height = app.screen.height;
    red.x = 340;
    red.y = -80;
    red.rotation = 5 * Math.PI/180
    red.alpha = 0;
    app.stage.removeChildAt(LAYER.UI6);
    app.stage.addChildAt(red, LAYER.UI6);

    //白条
    const white = PIXI.Sprite.from("../res/img/白条.png");
    white.width = app.screen.width;
    white.height = app.screen.height;
    white.x = 290;
    white.alpha = 0;
    app.stage.removeChildAt(LAYER.UI7);
    app.stage.addChildAt(white, LAYER.UI7);

    //文本
    const text = new PIXI.Text("", {
        fontFamily: "方正兰亭圆_GBK_中",  // 设置字体
        fontSize: 40,      // 设置字体大小
        fill: "#515050",     // 设置字体颜色（16进制RGB）
    });
    // 关键步骤：设置锚点为中心
    text.anchor.set(0.5); // 中心对齐
    text.x = app.screen.width / 2;
    text.x += 290;
    text.y = app.screen.height / 2;
    text.text = textContent;
    text.alpha = 0;
    app.stage.removeChildAt(LAYER.UI8);
    app.stage.addChildAt(text,LAYER.UI8);
    
    // 创建 GSAP 时间线（控制动画序列）
    const timeline = gsap.timeline();
    // 红条动画（500ms）
    timeline.to(red, {
        x: 0,
        y: 0,
        rotation: 0,
        alpha: 1,
        duration: duration,          
        ease: "power1.inOut" 
    }, 0);
    // 白条动画（与红条同时开始）
    timeline.to(white, {
        x: 0,                 
        alpha: 1,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);        
    // 文字动画
    timeline.to(text, {
        x: app.screen.width / 2,                 
        alpha: 1,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);         
    
    await sleep(duration * 1000);
    

    //显示1秒
    await sleep(showTime * 1000);


    // 创建 GSAP 时间线（控制动画序列）
    const timeline2 = gsap.timeline();
    // 红条动画（500ms）
    timeline2.to(red, {
        x: red.x - 230,
        y: red.x - 50,
        rotation: red.rotation + 3 * Math.PI/180,
        alpha: 0,
        duration: duration,          
        ease: "power1.inOut" 
    }, 0);
    // 白条动画（与红条同时开始）
    timeline2.to(white, {
        x: white.x - 230,                 
        alpha: 0,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);        
    // 文字动画
    timeline2.to(text, {
        x: text.x - 230,                 
        alpha: 0,          
        duration: duration,
        ease: "power1.inOut"       
    }, 0);         
    
    await sleep(duration * 1000 + 100);
}


export async function end(app, onBlack) {
    console.log(app.stage.children)
    app.stage.getChildAt(12).visible = false

    const duration = 0.2;

    const blackOverlay = new PIXI.Graphics();
    blackOverlay.beginFill(0x000000); // 纯黑色填充
    blackOverlay.drawRect(0, 0, app.screen.width, app.screen.height); // 覆盖整个屏幕
    blackOverlay.endFill();
    blackOverlay.alpha = 0; // 初始透明度为0（完全透明）
    app.stage.removeChildAt(LAYER.BLACK);
    app.stage.addChildAt(blackOverlay, LAYER.BLACK);
    
    //auto直接隐藏掉
    const auto = app.stage.getChildAt(LAYER.UI3);
    auto.alpha = 0;

    const textBox = app.stage.getChildAt(LAYER.UI1);
    const nameBox = app.stage.getChildAt(LAYER.UI2);
    const name = app.stage.getChildAt(LAYER.UI4);
    const text = app.stage.getChildAt(LAYER.UI5);


    // 创建 GSAP 时间线（控制动画序列）
    const timeline = gsap.timeline();
    timeline.to(textBox, {
        width:app.screen.width * 0.165,
        height:app.screen.height  *  0.165,
        x:800,
        y:765,
        duration: duration,          
        ease: "power1.inOut" 
    }, 0);
    timeline.to(nameBox, {
        width:app.screen.width * 0.165,
        height:app.screen.height  *  0.165,
        x:800,
        y:765,
        duration: duration,          
        ease: "power1.inOut" 
    }, 0);
    timeline.to(name.scale, {  
        x:0.165,
        y:0.165,             
        duration: duration,
        ease: "power1.inOut"       
    }, 0); 
    timeline.to(name, {  
        x:name.x + 614,
        y:name.y + 139,             
        duration: duration,
        ease: "power1.inOut"       
    }, 0);      
    timeline.to(text.scale, {  
        x:0.165,
        y:0.165,             
        duration: duration,
        ease: "power1.inOut"       
    }, 0);      
    timeline.to(text, {
        x:text.x + 605,
        y:text.y + 71,             
        duration: duration,
        ease: "power1.inOut"       
    }, 0);      

    await sleep(duration * 1000);

    text.alpha = 0;
    name.alpha = 0;
    textBox.alpha = 0;
    nameBox.alpha = 0;


    const duration2 = 0.8;
    gsap.to(blackOverlay, {
        alpha: 1,         // 目标透明度（100%）
        duration: duration2,       // 动画时长（秒）
        ease: "power2.in"
    },);

    await sleep(duration2 * 1000 );

    onBlack.call();

    //黑屏1s
    await sleep( 1 * 1000);

}

export async function hideBlack(app) {
    const duration2 = 0.8;
    const blackOverlay = app.stage.getChildAt(LAYER.BLACK);
    gsap.to(blackOverlay, {
        alpha: 0,         // 目标透明度（100%）
        duration: duration2,       // 动画时长（秒）
        ease: "power2.out"
    },);

    await sleep(duration2 * 1000);
}