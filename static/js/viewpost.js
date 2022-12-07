let query = window.location.search;
let param = new URLSearchParams(query);
let id = param.get('id');

$(document).ready(function(){
    view_post_get(id);
})

function view_post_get(id) {
            $.ajax({
                type: "get", 
                url: `/views/${id}`,
                success: function (response) {

                    let rows = response[0]['view_post_list']

                    let title = rows[0]['title']
                    let content = rows[0]['content']
                    let boardLike = rows[0]['liked']
                    let id = rows[0]['id']
                    let userId = rows[0]['user_id']
                    let file_url = rows[0]['file_url']
                    let time = rows[0]['created_at']


                    if(file_url != null) {
                        if(response[1] == 0){
                            let temp_html =  `<h1>${title}</h1>
                                                <h5>작성 시간 : ${time}</h5>
                                                <h5>${content}</h5>
                                                <img src="static/upload/image/${file_url}" width="100%" height="100%">
                                                <button onclick="delete_post(${id})" type="button" id="delete_post" class="btn btn-dark delete_ment">삭제</button>
                                                <button type="button" id="${id}" class="btn btn-dark recover"><a href="/temp_update?id=${id}">수정</a></button>
                                                <div>${boardLike}</div>
                                                <div>
                                                <a class="likebutton" onclick= "like(${id},${userId})">🤍</a>
                                                </div>`
                            $('#view_post').append(temp_html)
                        } else{ let temp_html =  `<h1>${title}</h1>
                                                   <h5>작성 시간 : ${time}</h5>        
                                                <h5>${content}</h5>
                                                <img src="static/upload/image/${file_url}" width="100%" height="100%">
                                                <button onclick="delete_post(${id})" type="button" id="delete_post" class="btn btn-dark delete_ment">삭제</button>
                                                <button type="button" id="${id}" class="btn btn-dark recover"><a href="/temp_update?id=${id}">수정</a></button>
                                                <div>${boardLike}</div>
                                                <div>
                                                <a class="likebutton" onclick= "like(${id},${userId})">❤️</a>
                                                </div>`
                            $('#view_post').append(temp_html)

                        }
                    }

                    else {
                        if(response[1] == 0){
                            let temp_html =  `<h1>${title}</h1>
                                               <h5>작성 시간 : ${time}</h5>        
                                                <h5>${content}</h5>
                                                <button onclick="delete_post(${id})" type="button" id="delete_post" class="btn btn-dark delete_ment">삭제</button>
                                                <button type="button" id="${id}" class="btn btn-dark recover"><a href="/temp_update?id=${id}">수정</a></button>
                                                <div>${boardLike}</div>
                                                <div>
                                                <a class="likebutton" onclick= "like(${id},${userId})">🤍</a>
                                                </div>`
                            $('#view_post').append(temp_html)
                        } else{ let temp_html =  `<h1>${title}</h1>
                                                <h5>작성 시간 : ${time}</h5>
                                                <h5>${content}</h5>
                                                <button onclick="delete_post(${id})" type="button" id="delete_post" class="btn btn-dark delete_ment">삭제</button>
                                                <button type="button" id="${id}" class="btn btn-dark recover"><a href="/temp_update?id=${id}">수정</a></button>
                                                <div>${boardLike}</div>
                                                <div>
                                                <a class="likebutton" onclick= "like(${id},${userId})">❤️</a>
                                                </div>`
                            $('#view_post').append(temp_html)

                        }
                    }
                }
                }
            );
        }

function delete_post(id) {
    $.ajax({
        type: "POST",
        url: "/post/delete",
        data: { id_give: id },
        success: function (response) {
            alert(response['msg'])
            location.href="/";
        }
    });
}

function cancle_viewpost() {
    location.href = "/";
}

function like(id,userId){
  const boardId = id
  const writerId = userId
  $.ajax({
    type: "POST",
    url: "/liked",
    data: {board_id_give : boardId, writer_id_give : writerId},
    success: function (response) {
      window.location.reload()
    }
  });
}