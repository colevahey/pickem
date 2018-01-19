function login(){
  // Future use in a login page... For now we will leave
  // it here

  uname = document.getElementById("username").value
  pword = document.getElementById("password").value
  console.log("Username:",uname,"Password:",pword)
}

function setgames(jsondata){
  for (let i=0;i<jsondata.games.length;i++){
    game = jsondata.games[i]

    let newgame = document.createElement("tr")
    let awayteam = document.createElement("td")
    let hometeam = document.createElement("td")
    let spread = document.createElement("td")

    hometeam.className = "home"
    hometeam.selected = false
    hometeam.onclick = function(){select(["home",i])}
    hometeam.onmouseover = function(){if (hometeam.selected == false){hometeam.style = "background-color:#707070"}}
    hometeam.onmouseout = function(){if (hometeam.selected == false){hometeam.style = "background-color:grey"}}
    if (game.homeTeam.rank < 99) {
      hometeam.innerHTML = "#" + game.homeTeam.rank + " "
    } else {
      hometeam.innerHTML = ""
    }
    hometeam.innerHTML += game.homeTeam.displayName
    let homeclubhouse = document.createElement("a")
    homeclubhouse.href = "http://www.espn.com/college-football/team/_/id/"+game.homeTeam.id
    homeclubhouse.target = "_blank"
    let homeimage = document.createElement("img")
    homeimage.src = game.homeTeam.logoUrl
    homeimage.height = "100"
    homeimage.style = "float:left;"
    homeclubhouse.appendChild(homeimage)
    hometeam.appendChild(homeclubhouse)

    spread.className = "versus"
    if (game.odds.spread != "N/A") {
      spread.innerHTML = game.odds.spread 
    } else {
      spread.innerHTML = game.scores.home + "  -  " + game.scores.away
    }

    awayteam.className = "away"
    awayteam.selected = false
    awayteam.onclick = function(){select(["away",i])}
    awayteam.onmouseover = function(){if (awayteam.selected == false){awayteam.style = "background-color:#707070"}}
    awayteam.onmouseout = function(){if (awayteam.selected == false){awayteam.style = "background-color:grey"}}
    if (game.awayTeam.rank < 99) {
      awayteam.innerHTML = "#" + game.awayTeam.rank + " "
    } else {
      awayteam.innerHTML = ""
    }
    awayteam.innerHTML += game.awayTeam.displayName 
    let awayclubhouse = document.createElement("a")
    awayclubhouse.href = "http://www.espn.com/college-football/team/_/id/"+game.awayTeam.id
    awayclubhouse.target = "_blank"
    let awayimage = document.createElement("img")
    awayimage.src = game.awayTeam.logoUrl
    awayimage.height = "100"
    awayimage.style = "float:right;"
    awayclubhouse.appendChild(awayimage)
    awayteam.appendChild(awayclubhouse)

    newgame.appendChild(hometeam)
    newgame.appendChild(spread)
    newgame.appendChild(awayteam)
    document.getElementById("gamestable").appendChild(newgame)
  }
}

function select(teamnum){
  hometeams = document.getElementsByClassName("home")
  awayteams = document.getElementsByClassName("away")
  if (teamnum[0] == "home") {
    if (hometeams[teamnum[1]].selected == false) {
      hometeams[teamnum[1]].style = "background-color:#ff2d2d;"
      hometeams[teamnum[1]].selected = true
      awayteams[teamnum[1]].style = "background-color:grey;"
      awayteams[teamnum[1]].selected = false
    } else {
      hometeams[teamnum[1]].style = "background-color:grey;"
      hometeams[teamnum[1]].selected = false
    }
  } else {
    if (awayteams[teamnum[1]].selected == false) {
      awayteams[teamnum[1]].style = "background-color:#ff2d2d;"
      awayteams[teamnum[1]].selected = true
      hometeams[teamnum[1]].style = "background-color:grey;"
      hometeams[teamnum[1]].selected = false
    } else {
      awayteams[teamnum[1]].style = "background-color:grey;"
      awayteams[teamnum[1]].selected = false
    }
  }
}
