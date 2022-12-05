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

function showBoard(){
  $.ajax({
    type: 'GET',
    url: `/liked/board`,
    data: {},
    success: function (response) {
      
      let title = response[0]['boardData']['title']
      let content = response[0]['boardData']['content']
      let fileUrl = response[0]['boardData']['file_url']
      let id = response[0]['boardData']['id']
      let userId = response[0]['boardData']['user_id']
      let boardLike = response[0]['boardData']['liked']
       
      if(response[1] == 0){
        let temp_html = `<div id ="boardId${id}">아이디 : ${id}<br>
                        제목 : ${title}<br>
                        내용 : ${content}<br>
                        파일 : ${fileUrl}<br>
                        User_id : ${userId}<br>
                        board count LIKE : ${boardLike}
                        <a class="likebutton" onclick= "like(${id},${userId})">🤍</a>
                      </div>`
      $('#board').append(temp_html)
      } else {
        let temp_html = `<div id ="boardId${id}">아이디 : ${id}<br>
                        제목 : ${title}<br>
                        내용 : ${content}<br>
                        파일 : ${fileUrl}<br>
                        User_id : ${userId}<br>
                        board count LIKE : ${boardLike}
                        <a class="likebutton" onclick= "like(${id},${userId})">❤️</a>
                      </div>`
      $('#board').append(temp_html)
      }
    }
  });
}