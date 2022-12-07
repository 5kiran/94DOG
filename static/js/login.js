document.cookie = 'safeCookie1=foo; SameSite=Lax';
document.cookie = 'safeCookie2=foo';
document.cookie = 'crossCookie=bar; SameSite=None; Secure';

function register_click() {
  const input_file = document.querySelector('#file_form');
  let data = new FormData(input_file);
  const check_email = document.getElementById('email').value;
  const check_password = document.getElementById('password').value;
  const check_name = document.getElementById('user_name').value;
  console.log(check_password);
  console.log(check_name);
  let emailRegExp =
    /^[A-Za-z0-9_]+[A-Za-z0-9]*[@]{1}[A-Za-z0-9]+[A-Za-z0-9]*[.]{1}[A-Za-z]{1,3}$/;

  if (user_name === '' || email === '' || password == '') {
    alert('모두 입력해주세요.');
  } else if (!emailRegExp.test(check_email)) {
    alert('이메일 형식이 올바르지 않습니다.');
  } else if (check_password.length > 30) {
    alert('패스워드의 길이를 줄여주세요.');
  } else if (check_name.length > 20) {
    alert('이름의 길이를 줄여주세요.');
  } else {
    $.ajax({
      type: 'POST',
      url: '/register/in',
      data: data,
      contentType: false,
      processData: false,
      success: function (response) {
        console.log(response);
        alert(response['msg']);
        window.location.href = '/login';
      },
    });
  }
}

function login_click() {
  const email = $('#email').val();
  const password = $('#password').val();

  if (email == '' || password == '') {
    alert('모두 입력해주세요.');
  } else {
    $.ajax({
      type: 'POST',
      url: '/login/in',
      data: {
        email_give: email,
        password_give: password,
      },
      success: function (response) {
        if (response['msg'] == '로그인 성공') {
          alert(response['msg']);
          window.location.href = '/';
        } else {
          alert(response['msg']);
          window.location.reload();
        }
      },
    });
  }
}

function email_click() {
  const email = $('#email').val();
  $.ajax({
    type: 'POST',
    url: '/email',
    data: {
      email_give: email,
    },
    success: function (response) {
      if (response['msg'] == '중복된 이메일입니다.') {
        alert(response['msg']);
      } else {
        alert(response['msg']);
      }
    },
  });
}
