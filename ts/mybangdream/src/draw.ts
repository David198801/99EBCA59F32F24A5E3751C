import * as PIXI from 'pixi.js'

window.PIXI = PIXI;

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

    app.stage.addChild(background);
}

const IntervalIds = {
    autoIntervalId: null
}
// 新增的drawUI函数
export async function drawUI(app) {
    const menu = PIXI.Sprite.from("../res/img/右上角菜单.png");
    menu.width = app.screen.width;
    menu.height = app.screen.height;
    app.stage.addChild(menu);

    const textBox = PIXI.Sprite.from("../res/img/姓名框和对话框.png");
    textBox.width = app.screen.width;
    textBox.height = app.screen.height;
    app.stage.addChild(textBox);


    const auto = PIXI.Sprite.from("../res/img/AUTO.png");
    auto.x = 1510;  // 设置X坐标
    auto.y = 785;  // 设置Y坐标
    auto.width = 150;
    auto.height = 50;
    app.stage.addChild(auto);
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

export async function clearApp(app) {
    app.stage.removeChildren().forEach(child => child.destroy());
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
    if(app.stage.children.length>6){
        app.stage.removeChildAt(6);
    }
    app.stage.addChildAt(text,6);
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
     if(app.stage.children.length>7){
        app.stage.removeChildAt(7);
    }
    app.stage.addChildAt(text,7);

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
