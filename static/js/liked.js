function like(postId,writer){
  const userId = document.getElementById('userId').value
  const boardId = postId
  const writerId = writer
  $.ajax({
    type: "POST",
    url: "/liked",
    data: {user_id_give : userId,board_id_give : boardId, writer_id_give : writerId},
    success: function (response) {
        alert(response["msg"])
        window.location.reload()
    }
  });
}

function showBoard(){
  $.ajax({
    type: 'GET',
    url: `/liked/board`,
    data: {},
    success: function (response) {
      console.log(response['boardData'])
      let title = response['boardData']['title']
      let content = response['boardData']['content']
      let fileUrl = response['boardData']['file_url']
      let id = response['boardData']['id']
      let userId = response['boardData']['user_id']
      let boardLike = response['boardData']['liked']


      let temp_html = `<div id ="boardId${id}">아이디 : ${id}<br>
                        제목 : ${title}<br>
                        내용 : ${content}<br>
                        파일 : ${fileUrl}<br>
                        User_id : ${userId}<br>
                        board count LIKE : ${boardLike}
                        <button onclick= "like(${id},${userId})" type="button" class="btn btn-dark">좋아요 </button>
                      </div>`
      $('#board').append(temp_html)
    
    }
  });
}