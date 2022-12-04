function showRank(){
  $.ajax({
    type: 'GET',
    url: `/liked/rank`,
    data: {},
    success: function (response) {
      let rows = response['likeRankList']

      for(let i in rows){
        let name = rows[i]['name']
        let rank = rows[i]['like_cnt']
        console.log(name,rank)

        let temp_html = `
                          <div id = "likeRank" >
                            <div>${i}위</div>
                            <div>${name}</div>
                            <div>${rank}개</div>
                          `
          $('#likeRankBoard').append(temp_html)
      }
    }
  });
}