let query = window.location.search;
let param = new URLSearchParams(query);
let id = param.get('id');

$(document).ready(function () {
  view_post_get(id);
});

function view_post_get(id) {
  $.ajax({
    type: 'GET',
    url: `/api/boards/${id}`,
    success: function (response) {
      if (
        response[0]['view_post_list'] == 0 ||
        response[0]['view_post_list'][0]['deleted'] == 1
      ) {
          alert('올바른 주소가 아닙니다. \n주소가 잘못입력되었거나 변경,또는 삭제되어 요청한 페이지를 읽을 수 없습니다..')
          location.href='/'

          // let empty_html = `<h1>올바른 주소가 아닙니다!!</h1>
          //                   <h5>주소가 잘못입력되었거나 변경,또는 삭제되어 요청한 페이지를 읽을 수 없습니다..</h5>`;
          // $('#mypost').append(empty_html);
      } else {
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

        document.querySelector('#post_title').value = title;
        document.querySelector('#post_name').value = name;
        document.querySelector('#post_time').value = new Date(time).toLocaleString();

        document.querySelector('#post_cnt').value = cnt;
        document.querySelector('#content').value = content;
        
        // 이미지
        if (file_url != null) {
          let temp_img_tag = `<img class="img-fluid" src="static/upload/image/${file_url}"></br>`;
          document.querySelector('#post_img').innerHTML = temp_img_tag;
        }

        // 좋아요
        document.querySelector('#likeCnt').value = boardLike;
        if (response[1] == 0) {
          document.querySelector('#like_btn').innerHTML = '좋아요 🤍';
        } else {
          document.querySelector('#like_btn').innerHTML = '좋아요 ❤️';
        }
        // 좋아요 기능
        document.querySelector('#like_btn').addEventListener('click', () => {
          like(id, userId);
        });

        // 삭제
        document.querySelector('#delete_post').addEventListener('click', () => {
          if (confirm('삭제하시겠습니까?')) {
            delete_post(id);
          }
        });
        // 수정
        document.querySelector('#update_post').addEventListener('click', ()=>{
          location.href = `/temp_update?id=${id}`;
        })
      }
    },
  });
}

function delete_post(id) {
  $.ajax({
    type: 'PATCH',
    url: '/api/boards/{id}',
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
    url: '/api/liked',
    data: { board_id_give: boardId, writer_id_give: writerId },
    success: function (response) {
      if (response['msg'] == 1) {
        alert('로그인이 필요합니다');
      }
      let likeCnt = response[0]['cnt']['liked'];
      // let heart = '❤️';
      // let noneheart = '🤍';
      // $('#likeCnt').html(likeCnt)
      if (response[1] === 0) {
        document.querySelector('#likeCnt').value = likeCnt;
        document.querySelector('#like_btn').innerHTML = '좋아요 🤍';
      } else {
        document.querySelector('#likeCnt').value = likeCnt;
        document.querySelector('#like_btn').innerHTML = '좋아요 ❤️';
      }
      showRank();
    },
  });
}
