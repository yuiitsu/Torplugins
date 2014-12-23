
if (typeof JGB == "undefined") var JGB = {};

/**
 * 发起请求
 * @params string strUrl 请求地址
 * @params string strType 请求类型
 * @params object objData 请求数据
 * @params function callBack 回调函数
 */
function request(strUrl, objParams, objData, callBack){
	if(objParams.button){
		var button = objParams.button
		var loading = new JGB.loading(button);
		loading.start();
	}
	objAjaxHandler = $.ajax({
		url: strUrl,
		type: objParams.type ? objParams.type : "GET",
		data: objData,
		async: objParams.async == 'false' ? false : true,
		dataType: objParams.dataType ? objParams.dataType : 'json'
	});

	objAjaxHandler.fail(function(){
	
	})

	objAjaxHandler.done(function(d){
		if($.isFunction(callBack)){
			callBack(d);
			if(loading){
				loading.over();
			}
		}
	})
}

/**
 * 提示层
 * @params strText string 提示内容
 * @params intStatus int 状态代码
 * @params intAutoClose int 是否自动关闭
 */
function tips(o, strText, intStatus, dicOption){
	var intId = JGB.random(10000, 99999);
	var dicType = {
		200: 'success',
	}
	var strType = dicType[intStatus] ? dicType[intStatus] : 'danger';
	var _html = '<div class="alert alert-'+ strType +' j-tips" id="alert_'+ intId +'">'+
		'<a href="#" class="close" data-dismiss="alert">&times;</a>'+
		strText +
	'</div>';

	if(dicOption['position']){
		var strPosition = dicOption['position'];
		if(strPosition == 'after'){
			o.after(_html);
		}
	}else{
		o.html(_html);
	}

	if(dicOption['autoClose']){
		var intAutoCloseTime = dicOption['autoClose'] ? dicOption['autoClose'] : 2000;
		setTimeout(function(){
			$("#alert_" + intId).fadeOut('normal', function(){
				$(this).remove();
			});
		}, intAutoCloseTime);
	}

	return intId;
}

/**
 * 弹出层
 * @params strTitle string 标题
 * @params strContent string 内容
 * @params callback function 回调函数
 */
function modal(strTitle, strContent, callback){
	var _html = '<div class="modal fade" id="modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">'+
		'<div class="modal-dialog">'+
			'<div class="modal-content">'+
				'<div class="modal-header">'+
					'<button type="button" class="close" data-dismiss="modal" aria-hidden="true">'+
						'&times;'+
					'</button>'+
					'<h4 class="modal-title">'+
						strTitle+
					'</h4>'+
				'</div>'+
				'<div class="modal-body">'+
					strContent+
				'</div>'+
				'<div class="modal-footer">'+
					'<button type="button" class="btn btn-default" data-dismiss="modal">取消</button>'+
					'<button type="button" class="btn btn-primary" id="modalPrimary">确定</button>'+
				'</div>'+
			'</div>'+
		'</div>'+
	'</div>';
	$('body').append(_html);
	$("#modal").modal('show');

	$("#modalPrimary").click(function(){
		if($.isFunction(callback)){
			callback();
		}
	});
}

/**
 * 加载
 */
JGB.loading = function(o){
	var _this = o;
	var strLoadingText = _this.attr('data-loading-text');
	var strText = _this.text();
	this.start = function(){
		_this.attr('disabled', true);
		_this.text(strLoadingText);
		_this.attr('data-loading-text', strText);
	}

	this.over = function(){
		_this.text(strText);
		_this.attr('data-loading-text', strLoadingText);
		_this.removeAttr('disabled');
	}
}


/**
 * 遮罩层
 */
JGB.mask = function(){
    var mask=$("#JGB_MASK");
    this.show=function(o,background,opacity){
		var background=background?background:'#ccc';
		var opacity=opacity?opacity:30;
		var opacityPoint=opacity/100;
		if(mask.length==0){
            $('body').append('<div id="JGB_MASK" style="position:absolute;background-color:'+background+';opacity: '+opacityPoint+';filter:alpha(opacity='+opacity+');"></div>');
        }
		if(o){
			var opt=o.offset();
			var oW=o.outerWidth();
			var oH=o.outerHeight();
        	$("#JGB_MASK").css({'display':'block','top':opt.top,'left':opt.left,'width':oW,'height':oH});
		}else{
			var clientWH=JGB.getScroll();
			var oW=clientWH['clientWidth'];
			var oH=clientWH['scrollHeight'];
        	$("#JGB_MASK").css({'display':'block','top':0,'left':0,'width':oW,'height':oH});
		}
    }
    
    this.hide=function(){
        $("#JGB_MASK").css('display','none');
    }
}

/**
 * 随机数
 */
JGB.random = function(intStart, intEnd){
	return Math.floor(intEnd * Math.random() + intStart);
}

/**
 * 全选
 */
JGB.selectAll = function(){
	$(".j-select-all").unbind('click').click(function(){
		var booSelectStatus = $(this).is(':checked');
		var strTarget = $(this).attr('data-target');
		if(booSelectStatus){
			$(strTarget).attr('checked', true);
		}else{
			$(strTarget).attr('checked', false);
		}
	});
}

/**
 * 提交表单
 * @params o obj 表单对象
 * @params dicParams dict 参数字典
 */
JGB.submit = function(o, dicParams, before, callback){
	var strAction = o.attr('action');
	var strData = o.serialize();

	if($.isFunction(before)){
		if(!before()){
			return false;
		}
	}

	dicSetting = {
		'type': dicParams['type'] ? dicParams['type'] : 'POST',
		'dataType': dicParams['dataType'] ? dicParams['dataType'] : 'json',
		'button': dicParams['button'] ? dicParams['button'] : ''
	}

	request(strAction, dicSetting, strData, callback);
}

/**
 * pop 提示层
 */
function D(o,txt,autoCloseTime){
    this.createDbox=function(){
        var dbox='<div id="dbox"><b class="dbox_arr_bg"></b><b class="dbox_arr"></b><div class="dbox_txt"></div></div>';
        $('body').append(dbox);
    }
    if($("#dbox").length<=0){
        this.createDbox();
    }
    //对象坐标
    var offset=o.offset();
    var left=offset.left;
    var top=offset.top;
    //对象宽
    var OW=o.outerWidth();
    
    $("#dbox").find("div.dbox_txt").html(txt);
    //计算大小
    var DW=$("#dbox").outerWidth();
    var DH=$("#dbox").outerHeight();
    if(DW>OW){
        var DL=-(DW-OW)/2;
    }else{
        var DL=(OW-DW)/2;
    }
    //箭头定位
    var AL=DW/2-8;
    $("#dbox").find("b.dbox_arr_bg").css('left',AL);
    $("#dbox").find("b.dbox_arr").css('left',AL);
    //定位
    var DT=-DH-4;
    $("#dbox").css({'left':left,'top':top,'margin-top':DT,'margin-left':DL,'display':'block'});
    var autoclose,
        actime=1000;
    if(autoCloseTime===0){
        autoclose=false;
    }else{
        autoclose=true;
        actime=autoCloseTime==undefined?actime:autoCloseTime;
    }
    if(autoclose){
        clearTimeout(D.DTimer);
        D.DTimer=setTimeout(function(){
            $("#dbox").fadeOut();
        },actime);
    }
    //隐藏提示
    this.close=function(){
        $("#dbox").fadeOut();
    }
}

$(function(){
	
	// 焦点选中
	$(".j-focus").unbind('click').click(function(){
		$(this).select();
	});
})
