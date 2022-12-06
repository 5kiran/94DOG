$(document).ready(function () {
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

// const tonowdate = getFormatDate(new Date()); // 오늘 날짜 지정
// console.log('현재시간은 :' + tonowdate)

function save_post() {
    const title = $('#title').val();
    const content = $('#content').val();
    const date = getFormatDate(new Date());

    if (title === '' || content === '') {
        console.log(title, content, date)
        alert('빈칸을 모두 채워주세요 T^T')
    } else {
        console.log(title, content, date)
        $.ajax({
            type: "POST",
            url: "/post",
            data: {
                title_give: title,
                content_give: content,
                data_give: date
            },
            success: function (response) {
                alert(response['msg'])
                location.href = "/";
            }
        });
    }
}

// function update_post() {
//     const title = $('#title').val();
//     const content = $('#content').val();
//     const id = $('#id').val();

//     if (id === '') {
//         alert('id 값은 빈칸일 수 없어요')
//     } else {
//         $.ajax({
//             type: "POST",
//             url: "/post/update",
//             data: {
//                 title_give: title,
//                 content_give: content,
//                 id_give: id
//             },
//             success: function (response) {
//                 alert(response['msg'])
//                 window.location.reload()
//             }
//         });
//     }
// }

// function delete_post() {
//     const id = $('#id').val();
//     if (id === '') {
//         alert('id 값은 빈칸일 수 없어요')
//     } else {
//         $.ajax({
//             type: "POST",
//             url: "/post/delete",
//             data: { id_give: id },
//             success: function (response) {
//                 alert(response['msg'])
//                 window.location.reload()
//             }
//         });
//     }
// }
// function show_post() {
//     $('#card').empty()
//     $.ajax({
//         type: "get",
//         url: "/post",
//         data: {},
//         success: function (response) {
//             let rows = response['show_post']

//             for (let i = 0; i < rows.length; i++) {
//                 let title = rows[i][1]
//                 let id = rows[i][0]
//                 let content = rows[i][2]
//                 let deleted = rows[i][5]
//                 let update_at = rows[i][4]
//                 let temp_html = ``
//                 if (deleted == 0) {
//                     temp_html = `<div class="card-header"><a href="/viewpost-layout?id=${id}">
//                                     ${title}</a>
//                                 </div>
//                                 <div class="card-body">                            
//                                     <p class="card-text">${content} , ${update_at}</p>`
//                 }

//                 $('#card').append(temp_html)

//             }
//         }
//     });
// }

function cancel_post() {
    location.href = "/";
}


