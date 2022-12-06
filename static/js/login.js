document.cookie = 'safeCookie1=foo; SameSite=Lax';
document.cookie = 'safeCookie2=foo';
document.cookie = 'crossCookie=bar; SameSite=None; Secure';

function register_click() {
  const input_file = document.querySelector('#file_form');
  let data = new FormData(input_file);
  if (user_name === '' || email === '' || password == '') {
    alert('모두 입력해주세요.');
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
