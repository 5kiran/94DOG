// $(document).ready(function () {
// })

function getFormatDate(date) {
  var year = date.getFullYear();
  var month = 1 + date.getMonth();
  month = month > 10 ? month : '0' + month; // 10이 넘지 않으면 앞에 0을 붙인다
  var day = date.getDate();
  day = day > 10 ? day : '0' + day; // 10이 넘지 않으면 앞에 0을 붙인다
  var hours = date.getHours();
  hours = hours > 10 ? hours : '0' + hours; // 10이 넘지 않으면 앞에 0을 붙인다
  var minutes = date.getMinutes();
  minutes = minutes > 10 ? minutes : '0' + minutes; // 10이 넘지 않으면 앞에 0을 붙인다
  var seconds = date.getSeconds();
  seconds = seconds > 10 ? seconds : '0' + seconds; // 10이 넘지 않으면 앞에 0을 붙인다

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function save_post() {
  const title = $('#title').val();
  const content = $('#content').val();
  const date = getFormatDate(new Date());

  if (title === '' || content === '') {
    console.log(title, content, date);
    alert('빈칸을 모두 채워주세요 T^T');
  } else {
    console.log(title, content, date);
    $.ajax({
      type: 'POST',
      url: '/post',
      data: {
        title_give: title,
        content_give: content,
        data_give: date,
      },
      success: function (response) {
        alert(response['msg']);
        location.href = '/';
      },
    });
  }
}

function cancel_post() {
  location.href = '/';
}
