function showRank() {
  $.ajax({
    type: 'GET',
    url: `/liked/rank`,
    data: {},
    success: function (response) {
      let rows = response['likeRankList'];
      let count = 0;
      for (let i in rows) {
        let name = rows[i]['name'];
        let rank = rows[i]['like_cnt'];
        count += 1;
        let temp_html = `
                          <div id = "likeRank" >
                            <div>${count}위</div> ${name}님 ❤️${rank}개
                          </div>
                          `;
        $('#likeRankBoard').append(temp_html);
      }
    },
  });
}
