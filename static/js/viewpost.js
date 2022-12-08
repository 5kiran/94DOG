let query = window.location.search;
let param = new URLSearchParams(query);
let id = param.get('id');

$(document).ready(function () {
  view_post_get(id);
});

function view_post_get(id) {
  $.ajax({
    type: 'get',
    url: `/views/${id}`,
    success: function (response) {
      let rows = response[0]['view_post_list'];

      let title = rows[0]['title'];
      let content = rows[0]['content'];
      let boardLike = rows[0]['liked'];
      let id = rows[0]['id'];
      let name = rows[0]['name'];
      let file_url = rows[0]['file_url'];
      let time = rows[0]['created_at'];
      let userId = rows[0]['user_id'];
      let cnt = rows[0]['viewcount'] + 1;

      document.querySelector('#post_title').innerHTML = title;
      document.querySelector('#post_time').innerHTML = time;
      document.querySelector('#post_name').innerHTML = name;
      document.querySelector('#post_cnt').innerHTML = cnt;
      document.querySelector('#likeCnt').innerHTML = `좋아요 갯수 :${boardLike}`;
      
      document.querySelector('#likeimg').addEventListener('click', ()=>{ like(id, userId); });

      if (response[1] == 0) {
        document.querySelector('#likeimg').innerHTML = '🤍';
      } else {
        document.querySelector('#likeimg').innerHTML = '❤️';
      }
      
      document.querySelector('#post_content').innerHTML = content;
      if (file_url != null) {
        let temp_img_tag = `<img src="static/upload/image/${file_url}" style="width:500px; height:500px;"></br>`;
        document.querySelector('#post_img').innerHTML = temp_img_tag;
      } 

      document.querySelector('#delete_post').addEventListener('click', ()=>{ 
        if (confirm('삭제하시겠습니까?')) {
          delete_post(id);
        }
      });
      document.querySelector('#update_post > a').href = `/temp_update?id=${id}`;
    },
  });
}

function delete_post(id) {
  $.ajax({
    type: 'POST',
    url: '/post/delete',
    data: { id_give: id },
    success: function (response) {
      alert(response['msg']);
      location.href = '/';
    },
  });
}

function cancle_viewpost() {
  location.href = '/';
}

function like(id, userId) {
  const boardId = id;
  const writerId = userId;
  $.ajax({
    type: 'POST',
    url: '/liked',
    data: { board_id_give: boardId, writer_id_give: writerId },
    success: function (response) {
        if(response['msg']== 1 ){
            alert('로그인이 필요합니다')
        }
        let likeCnt = '좋아요 갯수 :' +  String(response[0]['cnt']['liked']);
        let heart = '❤️'
        let noneheart = '🤍'
        // $('#likeCnt').html(likeCnt)
        if(response[1] === 0){
            $('#likeCnt').html(likeCnt)
            $('#likeimg').html(noneheart)
        }else{
            $('#likeCnt').html(likeCnt)
            $('#likeimg').html(heart)
        }
        showRank()
    }
  });
}
