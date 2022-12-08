document.cookie = 'safeCookie1=foo; SameSite=Lax';
document.cookie = 'safeCookie2=foo';
document.cookie = 'crossCookie=bar; SameSite=None; Secure';
let cnt = 0;

function register_click() {
  const input_file = document.querySelector('#file_form');
  let data = new FormData(input_file);
  const check_email = document.getElementById('register_email').value;
  const check_password = document.getElementById('register_password').value;
  const check_name = document.getElementById('user_name').value;
  let count = cnt;

  if (user_name === '' || check_email === '' || check_password === '') {
    alert('모두 입력해주세요.');
  } else if (check_password.length > 30) {
    alert('패스워드의 길이를 줄여주세요.');
  } else if (check_name.length > 20) {
    alert('이름의 길이를 줄여주세요.');
  } else if (count == 0) {
    alert('이메일 중복체크를 해주세요.');
  } else {
    $.ajax({
      type: 'POST',
      url: '/register',
      data: data,
      contentType: false,
      processData: false,
      success: function (response) {
        console.log(response);
        alert(response['msg']);
        window.location.href = '/';
      },
    });
  }
}

function email_click() {
  const email = $('#register_email').val();

  $.ajax({
    type: 'POST',
    url: '/email',
    data: {
      email_give: email,
    },
    success: function (response) {
      if (response['msg'] == '중복된 이메일입니다.') {
        alert(response['msg']);
      } else if (email == '') {
        alert('이메일을 작성해주세요.');
      } else {
        alert(response['msg']);
        cnt += 1;
        return cnt;
      }
    },
  });
}
