// ==UserScript==
// @name        仙台同学
// @namespace   Violentmonkey Scripts
// @match       *://shuukurafans.com/*/*/
// @grant       none
// @require     https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js
// @version     0.1
// @author      房医生
// @description 2020/5/11 下午7:43:00
// ==/UserScript==



//创建文件、a标签，触发点击
function exportRaw(name, data) {
	var urlObject = window.URL || window.webkitURL || window.mozURL || window.msURL;
	var export_blob = new Blob([data]);
	var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a");
	save_link.href = urlObject.createObjectURL(export_blob);
	save_link.download = name;
	save_link.click();
}

// 获取全文
async function getAllText() {
	var pageUrl = [
		'https://shuukurafans.com/index.php/category/ss/',
		'https://shuukurafans.com/index.php/category/web/',
		'https://shuukurafans.com/index.php/category/web/page/2/',
		'https://shuukurafans.com/index.php/category/web/page/3/'
	];
	
	
	var promises = pageUrl.map(function(url) {
		return $.ajax({
			type: "GET",
			url: url,
			dataType: "html"
		});
	});

	var responses = await Promise.all(promises);
	
	
	var chaptersUrls = [];
	responses.forEach(function(data) {
			$(data).find(".content article a.type-list-more").each(function() {
			chaptersUrls.push($(this).attr("href"));
		});
	});
	
	//反转了！！！
	chaptersUrls = chaptersUrls.reverse()
	
	
	console.log(chaptersUrls)

	

	var allText = "";

	promises = chaptersUrls.map(function(url) {
		return $.ajax({
			type: "GET",
			url: url,
			dataType: "html"
		});
	});

	responses = await Promise.all(promises);

	responses.forEach(function(data) {
		var text = $(data).find(".content header.entry-header.group h1.entry-title").text();
		text += '\n\n';
		text += $(data).find(".content div.entry-content div.entry.themeform").text();
		text += '\n\n';
		allText += text;
	});
	
	//特殊处理
	allText = allText.replace(/\t/g, "");

	return allText;
}

//获取书名，执行getAllText()获取内容，执行下载
async function download() {
	var fileName = $("div.mod.detail h1").text() + ".txt";
	var txt = await getAllText()
	exportRaw(fileName, txt);
}

download()
