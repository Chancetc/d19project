$(document).ready(function(){

	// 登录按钮
	$("#login-btn").click(function(){
		signInAccount()
	});
});

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
      console.log("url from server is:"+url)
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