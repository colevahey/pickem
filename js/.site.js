function login(){
  uname = document.getElementById("username").value
  pword = document.getElementById("password").value
  console.log(uname, pword)
}

function getweek(){
  let url = "https://cfb-scoreboard-api.herokuapp.com/v1/date/20171011"
  return url
}

function setgames(jsondata){
  awayTeams = document.getElementsByClassName("away")
  spreads = document.getElementsByClassName("versus")
  homeTeams = document.getElementsByClassName("home")
  for (i=0;i<spreads.length;i++){
    game = jsondata.games[i]

    homeTeams[i].selected = false
    homeTeams[i].innerHTML = game.homeTeam.displayName
    let newhomeimage = document.createElement("img");
    newhomeimage.src = game.homeTeam.logoUrl
    newhomeimage.height = "100"
    homeTeams[i].appendChild(newhomeimage)

    if (game.odds.spread != "N/A") {
      spreads[i].innerHTML = game.odds.spread 
    } else {
      spreads[i].innerHTML = game.scores.home + "  -  " + game.scores.away
    }

    homeTeams[i].selected = false
    awayTeams[i].innerHTML = game.awayTeam.displayName 
    let newawayimage = document.createElement("img");
    newawayimage.src = game.awayTeam.logoUrl
    newawayimage.height = "100"
    awayTeams[i].appendChild(newawayimage)
  }
}
