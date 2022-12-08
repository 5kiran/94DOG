function showRank() {
  $.ajax({
    type: 'GET',
    url: `/liked/rank`,
    data: {},
    success: function (response) {
      let likeRankList = response['likeRankList'];
      
      $('#likeRankBoard').empty();
      $('#likeRankBoard').append('<div><i class="fa-solid fa-ranking-star"></i>좋아요 랭킹</div>');

      for (let i=0;i<likeRankList.length;i++) {
        let writer_id = likeRankList[i]['writer_id'];
        let name = likeRankList[i]['name'];
        let rank = likeRankList[i]['like_cnt'];
        let show = `${i+1}위<br> ${name}님 ❤️${rank}개`;

        $('#likeRankBoard').append(`<div onclick="goRankBoards(${writer_id})" class="likeRank" style="cursor: pointer;">${show}</div>`);
      }
    },
  });
  // setTimeout(showRank(), 20000);
}

function goRankBoards(id) {
  setBoards2(1, id);
}

const setBoards2 = (page, user_id) => {
  let boards_uri = `/boards`;
  if (page != undefined) {
    boards_uri = `/boards?p=${page}`;
  }
  if (user_id != undefined) {
    if (page != undefined) {
      boards_uri = `/boards?u=${user_id}&p=${page}`;
    } else {
      boards_uri = `/boards?u=${user_id}`;
    }
  }
  $.ajax({
    type: "GET",
    url: boards_uri,
    data: {},
    success: (res) => {
      if (Object.keys(res.response.boards).length <= 0){
        $('#boards').append(`<h1>등록된 게시글이 없습니다.</h1>`);
      } else {
        if ( res.response.total_page === 0) {
          $('#boards').append(`<h1>등록된 게시글이 없습니다.</h1>`);
        } else {
          setBoardsContent2(res.response);
          setPagination2(res.response);
        }
      }
    }
  });
};

const setBoardsContent2 = (response) => {
  let temp = '';
  $('#boards').empty();
  response.boards.forEach((board) => {
    temp += `<a href="/viewpost-layout?id=${board.id}">
              <div class="card border-secondary border-2 mb-2" style="cursor: pointer;">
              <div class="d-flex">
                <div class="p-2 w-100">
                  <div class="card-body">
                    <h5 class="card-title">${board.title}</h5>
                    <p class="card-text">작성자:${board.name}   <br>조회수:${board.viewcount}</p>
                  </div>
                </div>
                <div class="p-2 flex-shrink-1" >
                  <img src="static/upload/image/${board.file_url}" onerror="this.onerror=null; this,src='static/images/default.png';" class="img-fluid rounded-start preview_image" >
                </div>
              </div>
            </div>
            </a>`;
  })
  $('#boards').append(temp);
};

const setPagination2 = (response) => {
  let page = parseInt(response.page);
  let total_page = parseInt(response.total_page);
  let start_page = parseInt(response.start_page);
  let end_page = parseInt(response.end_page);

  let temp = '';
  if (start_page != 1) {
    temp += `<li class="page-item" style="cursor: pointer;">
              <a class="page-link" onclick="setBoards2(${start_page-1}, ${response.boards[0].user_id})"><span aria-hidden="true">&laquo;</span></a>
            </li>`;
  } else {
    temp += `<li class="page-item disabled">
              <a class="page-link"><span aria-hidden="true">&laquo;</span></a>
            </li>`;
  }
  for (let i=start_page;i<=end_page;i++) {
    if (i == page) {
      temp += `<li class="page-item active" style="cursor: pointer;"><a class="page-link" onclick="setBoards2(${i}, ${response.boards[0].user_id})">${i}</a></li>`;
    } else {
      temp += `<li class="page-item" style="cursor: pointer;"><a class="page-link" onclick="setBoards2(${i}, ${response.boards[0].user_id})">${i}</a></li>`;
    }
  }
  if (end_page != total_page) {
    temp += `<li class="page-item" style="cursor: pointer;">
              <a class="page-link" onclick="setBoards2(${end_page+1}, ${response.boards[0].user_id})"><span aria-hidden="true">&raquo;</span></a>
            </li>`;
  } else {
    temp += `<li class="page-item disabled">
              <a class="page-link"><span aria-hidden="true">&raquo;</span></a>
            </li>`;
  }
  $('.pagination').empty();
  $('.pagination').append(temp);
};
