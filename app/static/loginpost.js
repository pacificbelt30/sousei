async function postForm() {
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

  pass.value = await digestMessage(pass.value);
  //(async() => {
    //pass.value = await digestMessage(pass.value);
    //console.log(pass.value);
  //})();

  console.log(pass.value);
  form.method = 'POST';
  form.action = 'http://localhost/auth/';
  form.appendChild(userid);
  form.appendChild(pass);
  form.appendChild(remember);
  document.body.appendChild(form);

  form.submit();
}

async function post_form_newpass() {
  let form = document.createElement('form');
  let userid = document.createElement('input');
  userid.type = 'hidden';
  userid.name = 'id';
  userid.value = document.getElementById('userid').value;
  let pass = document.createElement('input');
  pass.type = 'hidden';
  pass.name = 'password';
  if(document.getElementById('new_password').value == document.getElementById('new_password_re').value){
    pass.value = document.getElementById('new_password').value;
  }
  else{
    console.log('error');
    return ;
  }
  let remember = document.createElement('remember');
  remember.type = 'type';
  remember.name = 'remember';
  remember.value = true;

  pass.value = await digestMessage(pass.value);
  //(async() => {
    //pass.value = await digestMessage(pass.value);
    //console.log(pass.value);
  //})();

  console.log(pass.value);
  form.method = 'POST';
  form.action = 'http://localhost/auth/chpass';
  form.appendChild(userid);
  form.appendChild(pass);
  form.appendChild(remember);
  document.body.appendChild(form);

  form.submit();
}
