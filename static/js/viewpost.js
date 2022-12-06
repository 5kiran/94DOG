let query = window.location.search;
let param = new URLSearchParams(query);
let id = param.get('id');

$(document).ready(function(){
    view_post_get(id);
})

function view_post_get(id) {
    console.log(id + '번 게시글 페이지')
            $.ajax({
                type: "get", 
                url: `/views/${id}`,
                success: function (response) {
                    let rows = response['view_post_list']
                    console.log(rows)
                    let title = rows[0]['title']
                    let content = rows[0]['content']
                    let temp_html =  `<h1>${title}</h1>
                                        <h5>${content}</h5>
                                        <button onclick="delete_post(${id})" type="button" id="delete_post" class="btn btn-dark delete_ment">삭제</button>
                                        <button type="button" id="${id}" class="btn btn-dark recover"><a href="/temp_update?id=${id}">수정</a></button>`
                    $('#view_post').append(temp_html)
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

function popup_update() {

}