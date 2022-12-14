let query = window.location.search;
let param = new URLSearchParams(query);
let id = param.get('id');

$(document).ready(function () {
    preview(id) 
})

function getFormatDate(date) {
    var year = date.getFullYear();
    var month = (1 + date.getMonth());
    month = month > 10 ? month : '0' + month; // 10이 넘지 않으면 앞에 0을 붙인다
    var day = date.getDate();
    day = day > 10 ? day : '0' + day; // 10이 넘지 않으면 앞에 0을 붙인다
    var hours = date.getHours();
    hours = hours > 10 ? hours : '0' + hours; // 10이 넘지 않으면 앞에 0을 붙인다
    var minutes = date.getMinutes();
    minutes = minutes > 10 ? minutes : '0' + minutes; // 10이 넘지 않으면 앞에 0을 붙인다
    var seconds = date.getSeconds();
    seconds = seconds > 10 ? seconds : '0' + seconds; // 10이 넘지 않으면 앞에 0을 붙인다

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

function modi_post() {
    $('#board_id').val(id);
    const title = $('#title').val();
    const content = $('#content').val();
    // const date = getFormatDate(new Date());
    const input_file = document.querySelector('#file_form');
    let data = new FormData(input_file);

    if (title === '' || content === '') {
        alert('빈칸을 모두 채워주세요 T^T')
    } else {
        $.ajax({
            type: "PUT",
            url: "/api/boards/{id}",
            data: data,
            contentType: false,
            processData: false,
            success: function (response) {
                alert(response['msg'])
                location.href = `/viewpost-layout?id=${id}`;
            }
        });
    }
}

function cancel_post() {
    location.href = `/viewpost-layout?id=${id}`;
}

function preview(id) {
    $.ajax({
        type: "get", 
        url: `/preview/${id}`,
        success: function (response) {
                let rows = response['preview_list'][0];
                
                let title = rows['title'];
                let content = rows['content'];
                let file_url = rows['file_url'];

                $(`#title`).val(title);
                $(`#content`).val(content);

                if (file_url != null) {
                    document.querySelector('#post_file_preview').innerHTML 
                    = `<img src="static/upload/image/${file_url}" id="post_file_preview" style="max-width: 500px; max-height: 500px;">`;
                }
        }})}