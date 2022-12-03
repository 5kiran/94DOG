function like(idNum){
  const userId = document.getElementById('userId').value
  const boardId = idNum
  $.ajax({
    type: "POST",
    url: "/liked",
    data: {user_id_give : userId,board_id_give : boardId},
    success: function (response) {
        alert(response["msg"])
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
      let id = response['boardData'][1][0]
      let title = response['boardData'][1][1]
      let content = response['boardData'][1][2]
      let fileUrl = response['boardData'][1][3]
      let userId = response['boardData'][1][4]
      let boardLike = response['boardData'][1][5]
      let likeCount = response['boardData'][0]


      let temp_html = `<div id ="boardId${id}">아이디 : ${id}<br>
                        제목 : ${title}<br>
                        내용 : ${content}<br>
                        파일 : ${fileUrl}<br>
                        User_id : ${userId}<br>
                        board count LIKE : ${boardLike}
                        liked select count like : ${likeCount}
                        <button onclick= "like(${id})" type="button" class="btn btn-dark">좋아요 </button>
                      </div>`
      $('#board').append(temp_html)
    
    }
  });
}