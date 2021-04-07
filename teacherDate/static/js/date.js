var None = null;
var scr = document.getElementsByTagName("script"); //获取HTML传递过来的data
var class_data = scr[scr.length - 1].getAttribute("data"); //获取HTML传递过来的data,{'2021-03-15': [[3, 1, '2021-03-15 00:18:20', '2021-03-15 00:18:20', '2021-03-15 00:18:20', None, '2021-03-15 00:18:20'], [4, 1, '2021-03-15 00:18:23', '2021-03-15 00:18:23', '2021-03-15 00:18:23', None, '2021-03-15 00:18:23']]}
var class_dict = (new Function("return " + class_data))();  //还原json == eval
var uid = scr[scr.length - 1].getAttribute("uid");
var now_click_date = null;
/*判断某年是否是闰年*/
function isLeap(year) {
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
        return true;
    } else {
        return false;
    }
}

var monthDay = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

/*判断某年某月某日是星期几，默认日为1号*/
function whatDay(year, month, day = 1) {
    var sum = 0;
    sum += (year - 1) * 365 + Math.floor((year - 1) / 4) - Math.floor((year - 1) / 100) + Math.floor((year - 1) / 400) + day;
    for (var i = 0; i < month - 1; i++) {
        sum += monthDay[i];
    }
    if (month > 2) {
        if (isLeap(year)) {
            sum += 29;
        } else {
            sum += 28;
        }
    }
    return sum % 7;      //余数为0代表那天是周日，为1代表是周一，以此类推
}

var class_list = null;
onmessage = function (e) {
    class_list = e.data;
    // alert(class_list);
};

function month_time_sum(curYear, curMonth) {
    //显示日历时请求这个月的总共上课时间
    var min_month = ajax_req('/get_mounth_class_minutes',{'curYear':curYear,'curMonth':curMonth,'uid':uid});
    return min_month['min']
};

function ajax_req(url,data) {
    var result;
    $.ajax({
        async: false,   //同步请求
        type : "POST",
        url : url,
        dataType:"json",
        data: data, //"{'curYear':"+curYear+",'curMonth':"+curMonth+",'uid':"+uid+"}",
        success : function(da) {
            result=da;
        }
    });
    return result
}

/*显示日历*/
function showCld(year, month, firstDay) {
    var i;
    var tagClass = "";
    var nowDate = new Date();
    clear_table();//先清课表table
    var days;//从数组里取出该月的天数
    if (month == 2) {
        if (isLeap(year)) {
            days = 29;
        } else {
            days = 28;
        }
    } else {
        days = monthDay[month - 1];
    }
    min_month = month_time_sum(year,month);
    /*当前显示月份添加至顶部*/
    var topdateHtml = year + "年" + month + "月"+'('+min_month+'分钟)';
    var topDate = document.getElementById('topDate');
    topDate.innerHTML = topdateHtml;
    /*添加日期部分*/
    var tbodyHtml = '<tr>';
    for (i = 0; i < firstDay; i++) {//对1号前空白格的填充
        tbodyHtml += "<td></td>";
    }
    var changLine = firstDay;
    var now_month = true;
    for (i = 1; i <= days; i++) {//每一个日期的填充
        var dat = year + '-' + (Array(2).join(0) + month).slice(-2) + '-' + (Array(2).join(0) + i).slice(-2); //格式化这一天的日期，接下来作为key取值
        if (year == nowDate.getFullYear() && month == nowDate.getMonth() + 1 && i == nowDate.getDate()) {
            tagClass = "curDate";//当前日期对应格子
            now_click_date = dat; //标记当前所在位置日期
            add_table_tr(dat);  //时间是今天日期 先把今天的课展现出来
            now_month = false; // 如果找到今天日期，则代表不是上一个月或者下一个月翻页
        } else if (class_dict.hasOwnProperty(dat)) {  //将上过课的日期标记红色,(Array(2).join(0)+month).slice(-2) ：将单位数变成双位
            tagClass = "haveclass"
        } else {
            tagClass = "isDate";//普通日期对应格子，设置class便于与空白格子区分开来
        }
        tbodyHtml += "<td class=" + "'" + tagClass + "'" + " data_ye=" + "'" + year + "'" + " data_mo=" + "'" + month + "'" + " data_da=" + "'" + i + "'" + " id=" + "'" + i + "'" + " onclick=" + "'" + "add_event(this)" + "'" + ">" + i + "</td>";
        changLine = (changLine + 1) % 7;
        if (changLine == 0 && i != days) {//是否换行填充的判断
            tbodyHtml += "</tr><tr>";
        }
    }
    if (changLine != 0) {//添加结束，对该行剩余位置的空白填充
        for (i = changLine; i < 7; i++) {
            tbodyHtml += "<td></td>";
        }
    }//实际上不需要填充后方，但强迫症必须整整齐齐！
    tbodyHtml += "</tr>";
    var tbody = document.getElementById('tbody');
    tbody.innerHTML = tbodyHtml;
    if (now_month){//翻页时候默认展示当前月份1号
        t = 1;
        click_update_background_color(1);
        var dat = year + '-' + (Array(2).join(0) + month).slice(-2) + '-' + '01';
        clear_table();//先清空表数据，再重新加载
        now_click_date = dat; //标记当前点击所在位置日期
        add_table_tr(dat);
    }else {
        t = 1;
        click_update_background_color(nowDate.getDate());
    };
};

function add_event(date) {
    // 点击日历某一天,获取点击的日期，根据日期展示这一天的课程记录，也可以添加这一天的数据
    clear_table();//先清空表数据，再重新加载
    year = date.getAttribute("data_ye");
    month = date.getAttribute("data_mo");
    day = date.getAttribute("data_da");
    click_update_background_color(day);
    date = year + '-' + (Array(2).join(0) + month).slice(-2) + '-' + (Array(2).join(0) + day).slice(-2);
    now_click_date = date; //标记当前点击所在位置日期
    add_table_tr(date);
}

var t=1;
function click_update_background_color(x){
    //日期点击后改变背景色
    // 这个是判断第一次点击
  if(x==1&&t==1){
        document.getElementById(x).style.background="rgba(67,101,87,0.29)";
  }
   // 这个判断是防止重复点击
  else if (x != t) {
      try {
          document.getElementById(t).style.background = "transparent";
      } catch (e) {
          console.log(e)
      }
      document.getElementById(x).style.background = "rgba(67,101,87,0.29)";
  }
    t = x;
}

function nextMonth() {
    var topStr = document.getElementById("topDate").innerHTML;
    var pattern = /\d+/g;
    var listTemp = topStr.match(pattern);
    var year = Number(listTemp[0]);
    var month = Number(listTemp[1]);
    var nextMonth = month + 1;
    if (nextMonth > 12) {
        nextMonth = 1;
        year++;
    }
    document.getElementById('topDate').innerHTML = '';
    showCld(year, nextMonth, whatDay(year, nextMonth));
}

function preMonth() {
    var topStr = document.getElementById("topDate").innerHTML;
    var pattern = /\d+/g;
    var listTemp = topStr.match(pattern);
    var year = Number(listTemp[0]);
    var month = Number(listTemp[1]);
    var preMonth = month - 1;
    if (preMonth < 1) {
        preMonth = 12;
        year--;
    }
    document.getElementById('topDate').innerHTML = '';
    showCld(year, preMonth, whatDay(year, preMonth));
}

function add_table_tr(dat=null) {
    clear_table();//先清空table
    // var data_list =[[3, 1, '2021-03-15 00:18:20', '2021-03-15 08:10:20', '2021-03-15 22:18:20', None, '2021-03-15 00:18:20'], [4, 1, '2021-03-15 00:18:23', '2021-03-15 00:18:23', '2021-03-15 00:18:23', None, '2021-03-15 00:18:23']]
    if (class_dict.hasOwnProperty(dat)) {
      data_list = class_dict[dat];
    }else{
      data_list = [];
    }
    for (let i = 0; i < data_list.length; i++) {
        var item = data_list[i];
        var time_diff = diffTime(item[3], item[4]);
        if (time_diff){
            $("#news_table").append(
                '<tr>' +
                '<td style="white-space: nowrap;text-align:center;width: 80px;"><input style="font-size: 15px;background:rgba(233,15,5,0.71);" type="button" id="item_del" value="删除" itemid="'+item[0]+'" itkey="'+dat+'" onclick="delete_one_class(this)">' +
                                                                                '<input style="font-size: 15px;background:rgba(233,15,5,0.71);" type="button" id="fix" value="修改" itemid="'+item[0]+'" data="'+item+'" itkey="'+dat+'"></th>' +
                '<td style="white-space: nowrap;text-align:center;width: 200px;color: #c7f8cf" >' + item[3].split(' ')[1] + '</td>' +
                '<td style="white-space: nowrap;text-align:center;width: 200px;color: #c7f8cf" >' + item[4].split(' ')[1] + '</td>' +
                '<td style="hite-space: nowrap;text-align:center;width: 100px;color: #38f811" >' + time_diff + '</td>' +
                '<td style="white-space: nowrap;text-align:center;width: auto;color: #1ff8f0;word-wrap:break-word;word-break:break-all;" >' + item[5] + '</td>' +
                '</tr>');
        }
    }
    var data_list = now_click_date.split('-');  //重新加载日历月度总分钟数量
    update_month_title(data_list[0],data_list[1]);
}

//使用Jquery 删除,单行
function delete_one_class(obj){
    itkey = obj.getAttribute("itkey");
    itemid = obj.getAttribute("itemid");
    $(obj).parent().parent().parent()[0].removeChild($(obj).parent().parent()[0]);  // 删除一行
    class_dict = ajax_req('deloneclass',{'itemid':itemid,'uid':uid});//发送需要删除的数据到接口
    var data_list = now_click_date.split('-');  //重新加载日历月度总分钟数量
    update_month_title(data_list[0],data_list[1]);
    // $.post('deloneclass',{'itemid':itemid,'uid':uid},function(resultJSONObject){
    //     class_dict = resultJSONObject
    // })//发送需要删除的数据到接口
}


//时间差计算
/*
* startDate==>开始时间
* endDate==>结束时间
* 事例：diffTime(data.createTime,new Date())
*
* */
function diffTime(time1, time2) {
    //判断开始时间是否大于结束日期
    if (time1 > time2) {
        alert("开始时间不能大于结束时间！");
        return false;
    }
    //截取字符串，得到日期部分"2009-12-02",用split把字符串分隔成数组
    var begin1 = time1.substr(0, 10).split("-");
    var end1 = time2.substr(0, 10).split("-");
    //将拆分的数组重新组合，并实例成化新的日期对象
    var date1 = new Date(begin1[1] + -+begin1[2] + -+begin1[0]);
    var date2 = new Date(end1[1] + -+end1[2] + -+end1[0]);
    //得到两个日期之间的差值m，以分钟为单位
    //Math.abs(date2-date1)计算出以毫秒为单位的差值
    //Math.abs(date2-date1)/1000得到以秒为单位的差值
    //Math.abs(date2-date1)/1000/60得到以分钟为单位的差值
    var m = parseInt(Math.abs(date2 - date1) / 1000 / 60);
    //小时数和分钟数相加得到总的分钟数
    //time1.substr(11,2)截取字符串得到时间的小时数
    //parseInt(time1.substr(11,2))*60把小时数转化成为分钟
    var min1 = parseInt(time1.substr(11, 2)) * 60 + parseInt(time1.substr(14, 2));
    var min2 = parseInt(time2.substr(11, 2)) * 60 + parseInt(time2.substr(14, 2));
    //两个分钟数相减得到时间部分的差值，以分钟为单位
    var n = min2 - min1;
    //将日期和时间两个部分计算出来的差值相加，即得到两个时间相减后的分钟数
    var minutes = m + n;
    // var result = (Math.floor(minutes/60) + "小时" + (minutes%60) + "分" +"("+minutes+"分钟"+")");
    var result = minutes+"分钟";
    return result
}

function click_add() {
    //点击添加按钮后将添加课程展现出来
    var currentBtn = document.getElementById("add_class");
    currentBtn.style.visibility = "visible"; //显示添加div
    $("#select_time_1").val("");
    $("#select_time_2").val("");
}

function hidden_add_class() {
    //点击取消按钮后将添加课程隐藏
     var currentBtn = document.getElementById("add_class");
        currentBtn.style.visibility = "hidden"; //显示添加div
}

function clear_table() {
    //切换日期时 清空table表
    var t1 = document.getElementById("news_table");
    var rowNum = t1.rows.length;
    if (rowNum > 0) {
        for (i = 1; i < rowNum; i++) {
            t1.deleteRow(i);
            rowNum = rowNum - 1;
            i = i - 1;
        }
    }
}
function submin_add_class(){
    //点击确定按钮，将添加的课程数据发送到后台
    var start_end = document.getElementById('select_time_1').value;
    if (start_end != ""){
        var note = document.getElementById('select_time_2').value;
        $.post('insert',{'start_end':start_end,'note':note,'date':now_click_date,'uid':uid},function(resultJSONObject){
            class_dict = resultJSONObject;
            add_table_tr(now_click_date);
        });
        hidden_add_class();
        alert_add_scuueed();
    }
}

function update_month_title(year,month) {
    min_month = month_time_sum(year,month);
    /*当前显示月份添加至顶部*/
    console.log(min_month,year,month);
    var topdateHtml = year + "年" + month + "月"+'('+min_month+'分钟)';
    var topDate = document.getElementById('topDate');
    topDate.innerHTML = topdateHtml;
}

function alert_add_scuueed(){
    //点击确定后 提示添加成功
     var currentBtn = document.getElementById("gw");
                           currentBtn.style.visibility = "visible"; //显示
                            setTimeout(function (){
                             currentBtn.style.visibility = "hidden"
                            },1500)
};

laydate.render({ // 时间范围选择器
            elem: '#select_time_1'
            , type: 'time'
            ,range: true
        });




var curDate = new Date();
var curYear = curDate.getFullYear();
var curMonth = curDate.getMonth() + 1;
showCld(curYear, curMonth, whatDay(curYear, curMonth));
document.getElementById('right').onclick = function () {
    nextMonth();
};
document.getElementById('left').onclick = function () {
    preMonth();
};






//==========================================
// File:    star.js
// Title:   几何星空连线背景
//==========================================

// 可调参数
var BACKGROUND_COLOR = "rgba(0,43,54,1)";   // 背景颜色
var POINT_NUM = 100;                        // 星星数目
var POINT_COLOR = "rgba(255,255,255,0.7)";  // 点的颜色
var LINE_LENGTH = 10000;                    // 点之间连线长度(的平方)

// 创建背景画布
var cvs = document.createElement("canvas");
cvs.width = window.innerWidth;
cvs.height = window.innerHeight;
cvs.style.cssText = "\
    position:fixed;\
    top:0px;\
    left:0px;\
    z-index:-1;\
    opacity:1.0;\
    ";
document.body.appendChild(cvs);

var ctx = cvs.getContext("2d");

var startTime = new Date().getTime();

//随机数函数
function randomInt(min, max) {
    return Math.floor((max - min + 1) * Math.random() + min);
}

function randomFloat(min, max) {
    return (max - min) * Math.random() + min;
}

//构造点类
function Point() {
    this.x = randomFloat(0, cvs.width);
    this.y = randomFloat(0, cvs.height);

    var speed = randomFloat(0.3, 1.4);
    var angle = randomFloat(0, 2 * Math.PI);

    this.dx = Math.sin(angle) * speed;
    this.dy = Math.cos(angle) * speed;

    this.r = 1.2;

    this.color = POINT_COLOR;
}

Point.prototype.move = function () {
    this.x += this.dx;
    if (this.x < 0) {
        this.x = 0;
        this.dx = -this.dx;
    } else if (this.x > cvs.width) {
        this.x = cvs.width;
        this.dx = -this.dx;
    }
    this.y += this.dy;
    if (this.y < 0) {
        this.y = 0;
        this.dy = -this.dy;
    } else if (this.y > cvs.height) {
        this.y = cvs.height;
        this.dy = -this.dy;
    }
}

Point.prototype.draw = function () {
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.closePath();
    ctx.fill();
}

var points = [];

function initPoints(num) {
    for (var i = 0; i < num; ++i) {
        points.push(new Point());
    }
}

var p0 = new Point(); //鼠标
p0.dx = p0.dy = 0;
var degree = 2.5;
document.onmousemove = function (ev) {
    p0.x = ev.clientX;
    p0.y = ev.clientY;
}
document.onmousedown = function (ev) {
    degree = 5.0;
    p0.x = ev.clientX;
    p0.y = ev.clientY;
}
document.onmouseup = function (ev) {
    degree = 2.5;
    p0.x = ev.clientX;
    p0.y = ev.clientY;
}
window.onmouseout = function () {
    p0.x = null;
    p0.y = null;
}

function drawLine(p1, p2, deg) {
    var dx = p1.x - p2.x;
    var dy = p1.y - p2.y;
    var dis2 = dx * dx + dy * dy;
    if (dis2 < 2 * LINE_LENGTH) {
        if (dis2 > LINE_LENGTH) {
            if (p1 === p0) {
                p2.x += dx * 0.03;
                p2.y += dy * 0.03;
            } else return;
        }
        var t = (1.05 - dis2 / LINE_LENGTH) * 0.2 * deg;
        ctx.strokeStyle = "rgba(255,255,255," + t + ")";
        ctx.beginPath();
        ctx.lineWidth = 1.5;
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.closePath();
        ctx.stroke();
    }
    return;
}

//绘制每一帧
function drawFrame() {
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    ctx.fillStyle = BACKGROUND_COLOR;
    ctx.fillRect(0, 0, cvs.width, cvs.height);

    var arr = (p0.x == null ? points : [p0].concat(points));
    for (var i = 0; i < arr.length; ++i) {
        for (var j = i + 1; j < arr.length; ++j) {
            drawLine(arr[i], arr[j], 1.0);
        }
        arr[i].draw();
        arr[i].move();
    }

    window.requestAnimationFrame(drawFrame);
}

initPoints(POINT_NUM);
drawFrame();