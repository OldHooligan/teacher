function checkUser(){
				var username = document.getElementById("username").value;//文本框中的值，var是各种变量类型的集合
                var passwd = document.getElementById("passwd").value;//文本框中的值，var是各种变量类型的集合
                $.post('verification',{'u':username,'p':passwd},function(resultJSONObject){
                        if (resultJSONObject.state){
                            postCurrent('getclass',{'uid':resultJSONObject.uid,'name':resultJSONObject.name})
                        }else {
                           var currentBtn = document.getElementById("gw");
                           currentBtn.style.visibility = "visible"; //显示
                            setTimeout(function (){
                             currentBtn.style.visibility = "hidden"
                            },1500)
                        }
                })
			}

/**
 * form表单提交本页面打开
 * @param url
 * @param params
 */
function postCurrent(url,params){
    var form = $("<form method='post'></form>");
    var input;
    form.attr({"action":url});
    $.each(params,function (key,value) {
        input = $("<input type='hidden'>");
        input.attr({"name":key});
        input.val(value);
        form.append(input);
    });
    $(document.body).append(form);
    form.submit();
}