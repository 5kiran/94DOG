function register_click() {
  const name = $('#name').val();
  const email = $('#email').val();
  const password = $('#password').val();

  if (name == '' || email == '' || password == '') {
    alert('내용을 작성해주세요.');
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
