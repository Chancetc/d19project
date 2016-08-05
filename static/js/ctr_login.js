$(document).ready(function(){

	// 登录按钮
	$("#login-btn").click(function(){
		signInAccount()
	});
});

// 登录接口
function signInAccount(){
  
  userName = $("input#username-login-input").val();
  password = $("input#username-password-input").val();
  if (!userName) {
    showLoginAlertWithContent("error!","请至少输入一下用户名吧亲～");
    return ;
  }
  $.post("/signInByAjaxAction",{
    username:userName,
    password:password
  },function(data,status){
    if (data.retCode != 0) {
      showLoginAlertWithContent("error!",data.msg?data.msg:"未知错误，错误码:"+data.retCode);
    }else{
      url = data.data.url
      userName = data.data.userName
      userId = data.data.userId
      if (userName != null && userName != "") {
        setCookie('userName',userName,10);
      }
      if (userId != null && userId != "") {
        setCookie('userId',userId,10);
      }
      console.log("url from server is:"+url)
      console.log(data.data)
      window.location.href = url
    }
  });
}

function loginInputKeyUp(e) {

  hideLoginAlert();
  e.which = e.which || e.keyCode;
  if(e.which == 13) {
    // submit
    signInAccount()
  }
}

function showLoginAlertWithContent(tip,c){

  $("#login-alert-content").text(c);
  if (!tip) {
    tip = "warning!";
  }
  $("#login-alert-tip").text(tip);
  document.getElementById("login-alert").style.display="block";
}

function hideLoginAlert(){

  document.getElementById("login-alert").style.display="none";
}

function getCookie(c_name){
    
    if (document.cookie.length>0){ 
        c_start=document.cookie.indexOf(c_name + "=")
        if (c_start!=-1){ 
            c_start=c_start + c_name.length+1 
            c_end=document.cookie.indexOf(";",c_start)
            if (c_end==-1) c_end=document.cookie.length
                return unescape(document.cookie.substring(c_start,c_end))
        } 
    }
    return ""
}

function setCookie(c_name,value,expiredays){

    var exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays)
    document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : "; expires="+exdate.toGMTString())
}