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
        let name = likeRankList[i]['name'];
        let rank = likeRankList[i]['like_cnt'];
        let show = `${i+1}위<br> ${name}님 ❤️${rank}개`;

        $('#likeRankBoard').append(`<div class="likeRank">${show}</div>`);
      }
    },
  });
  // setTimeout(showRank(), 20000);
}

