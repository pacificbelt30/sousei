// ログイン情報をポストするためのやつ
function postForm() {
  if(!validation()){
    console.log('失敗');
    return false;
  }
  let form = document.createElement('form');
  let userid = document.createElement('input');
  userid.type = 'hidden';
  userid.name = 'id';
  userid.value = document.getElementById('userid').value;
  let pass = document.createElement('input');
  pass.type = 'hidden';
  pass.name = 'password';
  pass.value = document.getElementById('password').value;
  let remember = document.createElement('remember');
  remember.type = 'type';
  remember.name = 'remember';
  remember.value = true;

  //pass.value = await digestMessage(pass.value);
  pass.value = digestMessage_jsSHA(pass.value);
  //(async() => {
    //pass.value = await digestMessage(pass.value);
    //console.log(pass.value);
  //})();

  console.log(pass.value);
  form.method = 'POST';
  //form.action = 'http://localhost/auth/';
  form.action = '/auth/';
  form.appendChild(userid);
  form.appendChild(pass);
  form.appendChild(remember);
  document.body.appendChild(form);

  form.submit();
}

// パスワード変更時に使用する
function post_form_newpass() {
  let form = document.createElement('form');
  /*
  let userid = document.createElement('input');
  userid.type = 'hidden';
  userid.name = 'id';
  userid.value = document.getElementById('user_name').value;
  */
  let pass = document.createElement('input');
  pass.type = 'hidden';
  pass.name = 'password';
  pass_value = document.getElementById('password').value;
  repass_value = document.getElementById('password_re').value;
  if(pass_value == '' || repass_value == ''){
    console.log('error');
    return ;
  }
  else if(document.getElementById('password').value == document.getElementById('password_re').value){
    pass.value = document.getElementById('password_re').value;
  }
  else{
    console.log('error');
    return ;
  }
  let remember = document.createElement('remember');
  remember.type = 'type';
  remember.name = 'remember';
  remember.value = true;

  //pass.value = await digestMessage(pass.value);
  pass.value = digestMessage_jsSHA(pass.value);
  //(async() => {
    //pass.value = await digestMessage(pass.value);
    //console.log(pass.value);
  //})();

  console.log(pass.value);
  form.method = 'POST';
  //form.action = 'http://localhost/auth/chpass';
  form.action = '/auth/chpass';
  //form.appendChild(userid);
  form.appendChild(pass);
  form.appendChild(remember);
  document.body.appendChild(form);

  form.submit();
}

// 入力されたパスワードをsha256にし，入力欄を上書きする
function inputpassword_to_sha256(){
  pass_v = document.getElementById('password_v');
  pass = document.getElementById('password');
  pass.value = digestMessage_jsSHA(pass_v.value);
  console.log(pass.value);
  return true;
}

// 空かどうか
function validation(){
  let userid = document.getElementById('userid');
  let pass = document.getElementById('password');
  let flag = true;
  if(!userid.checkValidity()){
    document.getElementById('error_userid').innerHTML = '';
    document.getElementById('error_userid').innerHTML = '入力が不正です';
    document.getElementById('error_userid').color = 'red';
    document.getElementById('userid').style.border = "2px solid red";
    flag = false;
  }
  if(!pass.checkValidity()){
    document.getElementById('error_password').innerHTML = '';
    document.getElementById('error_password').innerHTML = '入力が不正です';
    document.getElementById('error_password').color = 'red';
    document.getElementById('password').style.border = "2px solid red";
    flag = false;
  }
  return flag;
}

