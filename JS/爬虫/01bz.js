// ==UserScript==
// @name        真导出第一版主
// @namespace   Violentmonkey Scripts
// @match       *://01bz.tel/*/*/
// @grant       none
// @require     https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js
// @version     0.1
// @author      房医生
// @description 2020/5/11 下午7:43:00
// ==/UserScript==



    (function () {

      //创建文件、a标签，触发点击
      function exportRaw(name, data) {
        var urlObject = window.URL || window.webkitURL || window.mozURL || window.msURL;
        var export_blob = new Blob([data]);
        var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a");
        save_link.href = urlObject.createObjectURL(export_blob);
        save_link.download = name;
        save_link.click();
      }

      //获取各页章节列表的链接
      function getChaptersPage() {
        var endPage = $("div.pagelistbox a.endPage").attr("href");
        var urlSplit = endPage.split("_")
        var endNum = urlSplit[1].replace("/", "");

        var pageListArray = new Array();
        var i;

        for (i = 1; i <= parseInt(endNum); i++) {
          pageListArray[i - 1] = location.protocol + "//" + location.hostname + urlSplit[0] + "_" + String(i) + "/";
        }
        return pageListArray;
      }


      //获取某一页章节列表内的章节链接
      function getOnePageChaptersList(pageUrl) {

        var xmlhttp;

        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", pageUrl, false);
        xmlhttp.overrideMimeType("text/html;charset=gbk");
        xmlhttp.send();
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
          var responseDoc = (new DOMParser()).parseFromString(xmlhttp.responseText, 'text/html');
          var responseBody = responseDoc.body;
          var chapterLabelList = $(responseBody).find("div.mod.block.update.chapter-list:eq(1) ul.list>li");
          var chapterLinksArray = new Array();
          var i;
          for (i = 0; i < chapterLabelList.length; i++) {
            chapterLinksArray[i] = new Array();
            chapterLinksArray[i][0] = chapterLabelList[i].firstChild.innerText;
            chapterLinksArray[i][1] = chapterLabelList[i].firstChild.getAttribute("href");
          }
          return chapterLinksArray;


        }

      }


      //获取所有章节链接
      function getChaptersLink() {
        var pageLinksArray = getChaptersPage();
        var chapterArray = new Array();
        var i, j, n;
        n = 0;
        for (i = 0; i < pageLinksArray.length; i++) {
          var chapterLinksArray = getOnePageChaptersList(pageLinksArray[i]);
          for (j = 0; j < chapterLinksArray.length; j++, n++) {
            chapterArray[n] = new Array();
            chapterArray[n][0] = chapterLinksArray[j][0];
            chapterArray[n][1] = location.protocol + "//" + location.hostname + chapterLinksArray[j][1];
          }

        }
        return chapterArray;
      }
      //getChaptersLink() 

      //替换png名称为对应文字
      function replacePng(text) {
        var wordDict = {
          'a1u1.png': '爱', 'b1u1.png': '棒', 'b2u2.png': '帮', 'b3u3.png': '暴', 'b4u4.png': '婊', 'b5u5.png': '逼', 'b6u6.png': '勃', 'c1u1.png': '操',
          'c2u2.png': '插', 'c3u3.png': '潮', 'c4u4.png': '处', 'c5u5.png': '唇', 'd1u0u0.png': '毒', 'd1u1.png': '蛋', 'd2u2.png': '弹', 'd3u3.png': '荡',
          'd4u4.png': '党', 'd5u5.png': '弟', 'd6u6.png': '嫡', 'd7u7.png': '丁', 'd8u8.png': '洞', 'd9u9.png': '杜', 'f1u1.png': '粉', 'f2u2.png': '缝',
          'f3u3.png': '腐', 'f4u4.png': '妇', 'g1u0u0.png': '国', 'g1u1.png': '干', 'g2u2.png': '肛', 'g3u3.png': '搞', 'g4u4.png': '高', 'g5u5.png': '宫',
          'g6u6.png': '共', 'g7u7.png': '狗', 'g8u8.png': '龟', 'g9u9.png': '棍', 'h1u1.png': '含', 'h2u2.png': '胡', 'h3u3.png': '秽', 'j1u0u0.png': '茎',
          'j1u1.png': '鸡', 'j1u1u1.png': '锦', 'j1u2u2.png': '九', 'j1u3u3.png': '厥', 'j1u4u4.png': '菊', 'j1u5u5.png': '具', 'j2u2.png': '纪', 'j3u3.png': '妓',
          'j4u4.png': '贱', 'j5u5.png': '奸', 'j6u6.png': '交', 'j7u7.png': '介', 'j8u8.png': '挤', 'j9u9.png': '精', 'k1u1.png': '坑', 'l1u0u0.png': '裸', 'l1u1.png': '凌',
          'l2u2.png': '流', 'l3u3.png': '漏', 'l4u4.png': '撸', 'l5u5.png': '颅', 'l6u6.png': '乱', 'l7u7.png': '露', 'l8u8.png': '轮', 'l9u9.png': '伦', 'm1u1.png': '马',
          'm2u2.png': '妈', 'm3u3.png': '麻', 'm4u4.png': '氓', 'm5u5.png': '美', 'm6u6.png': '蜜', 'm7u7.png': '灭', 'm8u8.png': '咪', 'm9u9.png': '母', 'n1u1.png': '奶',
          'n2u2.png': '内', 'n3u3.png': '嫩', 'n4u4.png': '尿', 'n5u5.png': '虐', 'n6u6.png': '奴', 'p1u1.png': '剖', 'p2u2.png': '炮', 'p3u3.png': '鹏', 'p4u4.png': '屁',
          'q1u1.png': '枪', 'q2u2.png': '情', 'q3u3.png': '亲', 'r2u2.png': '肉', 'r3u3.png': '辱', 'r4u4.png': '乳', 'rrrrrrrrrr.png': '日', 's14u4.png': '酸', 's1u0u0.png': '水',
          's1u1.png': '骚', 's1u1u1.png': '熟', 's1u2u2.png': '丝', 's1u3u3.png': '死', 's2u2.png': '色', 's3u3.png': '杀', 's4u4.png': '射', 's5u5.png': '呻', 's6u6.png': '舌',
          's7u7.png': '湿', 's8u8.png': '尸', 's9u9.png': '兽', 't1u1.png': '台', 't2u2.png': '涛', 't3u3.png': '舔', 't4u4.png': '童', 't5u5.png': '偷', 't6u6.png': '腿',
          't7u7.png': '吞', 't8u8.png': '臀', 'w1u1.png': '亡', 'w2u2.png': '未', 'w3u3.png': '温', 'x1u1.png': '席', 'x2u2.png': '吸', 'x4u4.png': '性', 'x5u5.png': '胸',
          'x6u6.png': '锡', 'x7u7.png': '穴', 'x8u8.png': '血', 'x9u9.png': '学', 'y1u1.png': '药', 'y1u1u1.png': '欲', 'y2u2.png': '摇', 'y3u3.png': '漪', 'y4u4.png': '阴',
          'y5u5.png': '淫', 'y6u6.png': '硬', 'y7u7.png': '吟', 'y8u8.png': '义', 'y9u9.png': '幼', 'z1u1.png': '宰', 'z2u2.png': '泽', 'z3u3.png': '斩', 'z4u4.png': '炸',
          'z5u5.png': '指', 'z6u6.png': '中', 'z7u7.png': '主', 'z8u8.png': '做', 'z9u9.png': '足','x3u3.png': '酰'}
        var pngText = text;
        for (var key in wordDict) {
          pngText = pngText.replace(new RegExp(key, 'g'), wordDict[key]);
        }
        return pngText;
      }


      //获取某一章节内容
      function loadChapterText(chapterUrl) {
        var chapterText = "";

        var i, j;

        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", chapterUrl, false);
        xmlhttp.overrideMimeType("text/html;charset=gbk");
        xmlhttp.send();
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
          var responseDoc = (new DOMParser()).parseFromString(xmlhttp.responseText, 'text/html');
          var responseBody = responseDoc.body;
          //替换单字png图片为图片名称
          var textP = $(responseBody).find("div.page-content.font-large>p");
          var imgLabel = $(textP).find("img");
          for (i = 0; i < imgLabel.length; i++) {
            $(imgLabel[i]).replaceWith(imgLabel[i].getAttribute("src").split("/")[3])
          }
          var brLabel = $(textP).find("br");
          for (i = 0; i < brLabel.length; i++) {
            $(brLabel[i]).replaceWith("\r\n")
          }
          var text = textP.text();
          chapterText += text;

          //获取章节其他part的链接
          var chapterOtherPartALabelList = $(responseBody).find("center.chapterPages>a");

          var chapterOtherPartArray = new Array();

          for (i = 1; i < chapterOtherPartALabelList.length; i++) {
            chapterOtherPartArray[i - 1] = location.href + chapterOtherPartALabelList[i].getAttribute("href");
          }


          if (chapterOtherPartArray.length != 0) {
            for (j = 0; j < chapterOtherPartArray.length; j++) {
              chapterPartUrl = chapterOtherPartArray[j];
              var xmlhttpPart;
              xmlhttpPart = new XMLHttpRequest();
              xmlhttpPart.open("GET", chapterPartUrl, false);
              xmlhttpPart.overrideMimeType("text/html;charset=gbk");
              xmlhttpPart.send();
              if (xmlhttpPart.readyState == 4 && xmlhttpPart.status == 200) {
                var responseDocPart = (new DOMParser()).parseFromString(xmlhttpPart.responseText, 'text/html');
                var responseBodyPart = responseDocPart.body;
                var textPPart = $(responseBodyPart).find("div.page-content.font-large>p");
                var imgLabelPart = $(textPPart).find("img");
                for (i = 0; i < imgLabelPart.length; i++) {
                  $(imgLabelPart[i]).replaceWith(imgLabelPart[i].getAttribute("src").split("/")[3])
                }
                var brLabelPart = $(textPPart).find("br");
                for (i = 0; i < brLabelPart.length; i++) {
                  $(brLabelPart[i]).replaceWith("\r\n");
                }
                var textPart = textPPart.text();
                chapterText += textPart;

              }
            }
          }
        }
        return chapterText
      }


      

      
      //获取全文
      function getAllText() {
        var chapterLinksArray = new Array();
        chapterLinksArray = getChaptersLink();

        var allText = "";

        var i;
        for (i = 0; i < chapterLinksArray.length; i++) {

          allText += "\r\n" + chapterLinksArray[i][0] + "\r\n";
          chapterUrl = chapterLinksArray[i][1];
          allText += "\r\n" + loadChapterText(chapterUrl) + "\r\n";
        }
        
        allText = replacePng(allText).replace(/ /g, " ").replace(/　/g, " ");
        
        
        return allText
      }


      //获取书名，执行getAllText()获取内容，执行下载
      function download() {
        var fileName = $("div.mod.detail h1").text() + ".txt";
        exportRaw(fileName, getAllText());
      }

      //添加按钮，绑定download()
      function addButton() {
        var btn = document.createElement("BUTTON");
        var t = document.createTextNode("抓取txt");
        btn.onclick = download;
        btn.appendChild(t);
        $("div.ft").prepend(btn);
      }
      addButton();



    })()
