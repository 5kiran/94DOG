document.cookie = 'safeCookie1=foo; SameSite=Lax';
document.cookie = 'safeCookie2=foo';
document.cookie = 'crossCookie=bar; SameSite=None; Secure';

function register_click() {
  const name = $('#name').val();
  const email = $('#email').val();
  const password = $('#password').val();

  if (name == '' || email == '' || password == '') {
    alert('모두 입력해주세요.');
  } else {
    $.ajax({
      type: 'POST',
      url: '/register/in',
      data: {
        name_give: name,
        email_give: email,
        password_give: password,
      },
      success: function (response) {
        alert(response['msg']);
        window.location.reload();
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
    });
  }
}
