const setuser = _ => {
  let urlParams = new URLSearchParams(window.location.search)
  let username = ""
  try {
    username = urlParams.get('uname').toUpperCase()
  }
  catch(err) {
    document.write("Error 001: No username specified")
  }
  user = document.createElement("p")
  user.id = "username"
  user.innerHTML = username
  user.style.color = "white"
  user.style.float = "right"
  navigationbar = document.querySelector("#navbar")
  navigationbar.appendChild(user)
}

const getdate = _ => {
  let gamedate = new Date()
  let today = new Date()
  gamedate.setDate(gamedate.getDate()+0.5)
  gamedate.setDate(gamedate.getDate() + (6+(7-gamedate.getDay())) % 7)

  year = gamedate.getYear()+1900

  month = gamedate.getMonth()+1
  switch(month>9){
    case false:
      month = ['0',month].join("")
  }

  day = gamedate.getDate()
  switch(day>9){
    case false:
      day = ['0',day].join("")
  }

  if (today < gamedate){
    gamedate = "20180901"
  } else {
    gamedate = [year,month,day].join("")
  }

  return gamedate
}
getdate()

const fetchdata = date => {
  fetch('http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?calendartype=blacklist&dates='+date).then(function(response){response.json().then(function(data){setgames(data)})})
}

const setgames = gamedata => {

  for (let i=0;i<gamedata.events.length;i++){
    let game = gamedata.events[i].competitions[0]
    let homedata = game.competitors[0]
    let awaydata = game.competitors[1]

    let newgame = document.createElement("tr")
    newgame.className = "game"

    let awayTeam = document.createElement("td")
    let homeTeam = document.createElement("td")
    let spread = document.createElement("td")

    homeTeam.className = "home"
    homeTeam.selected = false
    homeTeam.onclick = function(){select(["home",i])}
    homeTeam.onmouseover = function(){if (homeTeam.selected == false){homeTeam.style = "background-color:#707070"}; this.style.cursor = "pointer"}
    homeTeam.onmouseout = function(){if (homeTeam.selected == false){homeTeam.style = "background-color:grey"}; this.style.cursor = "default"}
    if (homedata.curatedRank.current < 99 && homedata.curatedRank.current != 0) {
      homeTeam.innerHTML = "#" + homedata.curatedRank.current + " "
    } else {
      homeTeam.innerHTML = ""
    }
    homeTeam.innerHTML += homedata.team.displayName
    let homeclubhouse = document.createElement("a")
    homeclubhouse.href = homedata.team.links[0].href
    homeclubhouse.target = "_blank"
    let homeimage = document.createElement("img")
    homeimage.src = homedata.team.logo
    homeimage.height = "100"
    homeimage.style = "float:left;"
    homeclubhouse.appendChild(homeimage)
    homeTeam.appendChild(homeclubhouse)

    spread.className = "versus"
    if (game.status.type.completed != true) {
      //spread.innerHTML = game.odds.spread 
      spread.innerHTML = "N/A"
    } else {
      spread.innerHTML = homedata.score + "  -  " + awaydata.score
    }

    awayTeam.className = "away"
    awayTeam.selected = false
    awayTeam.onclick = function(){select(["away",i])}
    awayTeam.onmouseover = function(){if (awayTeam.selected == false){awayTeam.style = "background-color:#707070"}; this.style.cursor = "pointer"}
    awayTeam.onmouseout = function(){if (awayTeam.selected == false){awayTeam.style = "background-color:grey"}; this.style.cursor = "default"}
    if (awaydata.curatedRank.current < 99 && awaydata.curatedRank.current != 0) {
      awayTeam.innerHTML = "#" + awaydata.curatedRank.current + " "
    } else {
      awayTeam.innerHTML = ""
    }
    awayTeam.innerHTML += awaydata.team.displayName
    let awayclubhouse = document.createElement("a")
    awayclubhouse.href = awaydata.team.links[0].href
    awayclubhouse.target = "_blank"
    let awayimage = document.createElement("img")
    awayimage.src = awaydata.team.logo
    awayimage.height = "100"
    awayimage.style = "float:right;"
    awayclubhouse.appendChild(awayimage)
    awayTeam.appendChild(awayclubhouse)

    newgame.appendChild(homeTeam)
    newgame.appendChild(spread)
    newgame.appendChild(awayTeam)
    document.querySelector("#gamestable").appendChild(newgame)
  }
}

const select = teamnum => {
  homeTeams = document.getElementsByClassName("home")
  awayTeams = document.getElementsByClassName("away")
  if (teamnum[0] == "home") {
    if (homeTeams[teamnum[1]].selected == false) {
      homeTeams[teamnum[1]].style = "background-color:#ff2d2d;"
      homeTeams[teamnum[1]].selected = true
      awayTeams[teamnum[1]].style = "background-color:grey;"
      awayTeams[teamnum[1]].selected = false
    } else {
      homeTeams[teamnum[1]].style = "background-color:grey;"
      homeTeams[teamnum[1]].selected = false
    }
  } else {
    if (awayTeams[teamnum[1]].selected == false) {
      awayTeams[teamnum[1]].style = "background-color:#ff2d2d;"
      awayTeams[teamnum[1]].selected = true
      homeTeams[teamnum[1]].style = "background-color:grey;"
      homeTeams[teamnum[1]].selected = false
    } else {
      awayTeams[teamnum[1]].style = "background-color:grey;"
      awayTeams[teamnum[1]].selected = false
    }
  }
}

const finalcheck = _ => { 
  let games = document.getElementsByClassName("game")
  let totalselected = 0
  let notselected = "" 
  let selections = {"Username":document.querySelector("#username").innerHTML,"Game Selections":{}}
  for (let i=0; i<games.length; i++) {
    let game = games[i]
    switch (game.cells[0].selected){
      case true:
        console.log("Game",i+1,"home selected")
        totalselected += 1
        selections["Game Selections"]["Game " + i] = "HOME"
        break
      case false:
        switch (game.cells[2].selected){
          case true:
            console.log("Game",i+1,"away selected")
            totalselected += 1
            selections["Game Selections"]["Game " + i] = "AWAY"
            break
          case false:
            console.log("NO TEAM SELECTED GAME",i+1)
            notselected += i+1+" "
            break
        }
    }
  }
  console.log(selections)
  if (totalselected != 25){
    alert("NOT ALL GAMES SELECTED\nPlease make selections for games:\n"+notselected)
  } else {
    console.log(selections)
    alert("Thank you for making your selections")
    console.log(toString(selections))
    download([JSON.stringify(selections)], 'selections.json', 'text/plain')
  }
}

const download = (content, fileName, contentType) => {
    let a = document.createElement("a")
    let file = new Blob(content, {type: contentType})
    a.href = URL.createObjectURL(file)
    a.download = fileName
    a.click()
}
