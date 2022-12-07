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
