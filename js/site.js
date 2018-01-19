function login(){
  // Future use in a login page... For now we will leave
  // it here

  uname = document.getElementById("username").value
  pword = document.getElementById("password").value
  console.log("Username:",uname,"Password:",pword)
}

function getdate(){
  gamedate = "20171028"
  return gamedate 
}

function fetchdata(date){
  fetch('http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?calendartype=blacklist&dates='+date).then(function(response){response.json().then(function(data){setgames(data)})})
}

function setgames(gamedata){

  for (let i=0;i<gamedata.events.length;i++){
    let game = gamedata.events[i].competitions[0]
    let homedata = game.competitors[0]
    let awaydata = game.competitors[1]

    let newgame = document.createElement("tr")
    let awayteam = document.createElement("td")
    let hometeam = document.createElement("td")
    let spread = document.createElement("td")


    hometeam.className = "home"
    hometeam.selected = false
    hometeam.onclick = function(){select(["home",i])}
    hometeam.onmouseover = function(){if (hometeam.selected == false){hometeam.style = "background-color:#707070"}}
    hometeam.onmouseout = function(){if (hometeam.selected == false){hometeam.style = "background-color:grey"}}
    if (homedata.curatedRank.current < 99) {
      hometeam.innerHTML = "#" + homedata.curatedRank.current + " "
    } else {
      hometeam.innerHTML = ""
    }
    hometeam.innerHTML += homedata.team.displayName
    let homeclubhouse = document.createElement("a")
    homeclubhouse.href = homedata.team.links[0].href
    homeclubhouse.target = "_blank"
    let homeimage = document.createElement("img")
    homeimage.src = homedata.team.logo
    homeimage.height = "100"
    homeimage.style = "float:left;"
    homeclubhouse.appendChild(homeimage)
    hometeam.appendChild(homeclubhouse)

    spread.className = "versus"
    if (game.status.type.completed != true) {
      spread.innerHTML = game.odds.spread 
    } else {
      spread.innerHTML = homedata.score + "  -  " + awaydata.score
    }

    awayteam.className = "away"
    awayteam.selected = false
    awayteam.onclick = function(){select(["away",i])}
    awayteam.onmouseover = function(){if (awayteam.selected == false){awayteam.style = "background-color:#707070"}}
    awayteam.onmouseout = function(){if (awayteam.selected == false){awayteam.style = "background-color:grey"}}
    if (awaydata.curatedRank.current < 99) {
      awayteam.innerHTML = "#" + awaydata.curatedRank.current + " "
    } else {
      awayteam.innerHTML = ""
    }
    awayteam.innerHTML += awaydata.team.displayName
    let awayclubhouse = document.createElement("a")
    awayclubhouse.href = awaydata.team.links[0].href
    awayclubhouse.target = "_blank"
    let awayimage = document.createElement("img")
    awayimage.src = awaydata.team.logo
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

