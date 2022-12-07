// $(document).ready(function () {
// })

function save_post() {

  // const title = $('#title').val();
  // const content = $('#content').val();

  const input_file = document.querySelector('#file_form');
  let data = new FormData(input_file);
  const title_give = document.getElementById('title').value;
  const content_give = document.getElementById('content').value;

  if (title === '' || content === '') {
    alert('빈칸을 모두 채워주세요 T^T');
  } else {
    $.ajax({
      type: 'POST',
      url: '/post',
      data: data,
      contentType: false,
      processData: false,
      success: function (response) {
        alert(response['msg']);
        location.href = '/';
      },
    });
  }
}

function like(postId,writer){
  const boardId = postId
  const writerId = writer
  $.ajax({
    type: "POST",
    url: "/liked",
    data: {board_id_give : boardId, writer_id_give : writerId},
    success: function (response) {
      window.location.reload()
    }
  });
}
