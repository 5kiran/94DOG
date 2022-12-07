function showRank() {
  $.ajax({
    type: 'GET',
    url: `/liked/rank`,
    data: {},
    success: function (response) {
      let oneName = response['likeRankList'][0]['name']
      let oneRank = response['likeRankList'][0]['like_cnt']
      let oneShow = `1위<br> ${oneName}님 ❤️${oneRank}개`

      let twoName = response['likeRankList'][1]['name']
      let twoRank = response['likeRankList'][1]['like_cnt']
      let twoShow = `2위<br> ${twoName}님 ❤️${twoRank}개`

      let threeName = response['likeRankList'][2]['name']
      let threeRank = response['likeRankList'][2]['like_cnt']
      let threeShow = `3위<br> ${threeName}님 ❤️${threeRank}개`

      let fourName = response['likeRankList'][3]['name']
      let fourRank = response['likeRankList'][3]['like_cnt']
      let fourShow = `4위<br> ${fourName}님 ❤️${fourRank}개`

      let fiveName = response['likeRankList'][4]['name']
      let fiveRank = response['likeRankList'][4]['like_cnt']
      let fiveShow = `5위<br> ${fiveName}님 ❤️${fiveRank}개`

      $('.rank1').html(oneShow)
      $('.rank2').html(twoShow)
      $('.rank3').html(threeShow)
      $('.rank4').html(fourShow)
      $('.rank5').html(fiveShow)
    },
  });
  // setTimeout(showRank(), 20000);
}

