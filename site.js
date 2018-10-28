const setUser = _ => {
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

const getDate = _ => {
  let gameDate = new Date()
  let today = new Date()

  // Get the date of the next Saturday
  gameDate.setDate(gameDate.getDate()+0.5)
  gameDate.setDate(gameDate.getDate() + (6+(7-gameDate.getDay())) % 7)

  year = gameDate.getYear()+1900
  month = gameDate.getMonth()+1

  if (month < 9) {
    month = `0${month}`
  }

  day = gameDate.getDate()
  if (day < 9){
    day = `0${day}`
  }

  gameDate = `${year}${month}${day}`

  return gameDate
}

const fetchData = async date => {
  let response = await fetch('http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?calendartype=blacklist&dates='+date)
  let data = await response.json()
  setGames(data)
}

const setGames = gameData => {

  for (let i=0;i<gameData.events.length;i++){
    let game = gameData.events[i].competitions[0]
    let homeData = game.competitors[0]
    let awayData = game.competitors[1]

    let newGame = document.createElement("tr")
    newGame.className = "game"

    let awayTeam = document.createElement("td")
    let homeTeam = document.createElement("td")
    let spread = document.createElement("td")

    homeTeam.className = "home"
    homeTeam.selected = false
    //homeTeam.onclick = function(){select(["home",i])}
    homeTeam.onclick = _ => select(["home",i])
    
    homeTeam.onmouseover = e => {
      if (e.target.selected == false) {
        e.target.style = "background-color:#707070"
      }
      e.target.style.cursor = "pointer"
    }
    homeTeam.onmouseout = e => {
      if (e.target.selected == false){
        e.target.style = "background-color:grey"
      }
      e.target.style.cursor = "default"
    }

    if (homeData.curatedRank.current < 99 && homeData.curatedRank.current != 0) {
      homeTeam.innerHTML = "#" + homeData.curatedRank.current + " "
    } else {
      homeTeam.innerHTML = ""
    }
    homeTeam.innerHTML += homeData.team.displayName
    let homeClubhouse = document.createElement("a")
    homeClubhouse.href = homeData.team.links[0].href
    homeClubhouse.target = "_blank"
    let homeImage = document.createElement("img")
    homeImage.src = homeData.team.logo
    homeImage.height = "100"
    homeImage.style = "float:left;"
    homeClubhouse.appendChild(homeImage)
    homeTeam.appendChild(homeClubhouse)

    awayTeam.className = "away"
    awayTeam.selected = false
    awayTeam.onclick = function(){select(["away",i])}
    awayTeam.onmouseover = function(){if (awayTeam.selected == false){awayTeam.style = "background-color:#707070"}; this.style.cursor = "pointer"}
    awayTeam.onmouseout = function(){if (awayTeam.selected == false){awayTeam.style = "background-color:grey"}; this.style.cursor = "default"}
    if (awayData.curatedRank.current < 99 && awayData.curatedRank.current != 0) {
      awayTeam.innerHTML = "#" + awayData.curatedRank.current + " "
    } else {
      awayTeam.innerHTML = ""
    }
    awayTeam.innerHTML += awayData.team.displayName
    let awayClubhouse = document.createElement("a")
    awayClubhouse.href = awayData.team.links[0].href
    awayClubhouse.target = "_blank"
    let awayImage = document.createElement("img")
    awayImage.src = awayData.team.logo
    awayImage.height = "100"
    awayImage.style = "float:right;"
    awayClubhouse.appendChild(awayImage)
    awayTeam.appendChild(awayClubhouse)

    spread.className = "versus"
    if (game.status.type.completed != true) {
      if (game.odds) {
        spread.innerHTML = game.odds[0].details 
      } else {
        spread.innerHTML = "EVEN"
      }
    } else {
      spread.innerHTML = homeData.score + "  -  " + awayData.score
    }

    newGame.appendChild(homeTeam)
    newGame.appendChild(spread)
    newGame.appendChild(awayTeam)
    document.querySelector("#gamestable").appendChild(newGame)

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

const finalCheck = gameDate => { 
  let games = document.getElementsByClassName("game")
  let totalSelected = 0
  let notSelected = "" 
  let selections = {"Username":document.querySelector("#username").innerHTML}
  selections[gameDate] = {}
  for (let i=0; i<games.length; i++) {
    selections[gameDate]["Game"+i] = {}
    let game = games[i]
    switch (game.cells[0].selected){
      case true:
        console.log("Game",i+1,"home selected")
        totalSelected += 1
        selections[gameDate]["Game" + i]["team"] = "HOME"
        selections[gameDate]["Game" + i]["spread"] = game.querySelector(".versus").innerHTML
        break
      case false:
        switch (game.cells[2].selected){
          case true:
            console.log("Game",i+1,"away selected")
            totalSelected += 1
            selections[gameDate]["Game" + i]["team"] = "AWAY"
            selections[gameDate]["Game" + i]["spread"] = game.querySelector(".versus").innerHTML
            break
          case false:
            console.log("NO TEAM SELECTED GAME",i+1)
            notSelected += i+1+" "
            break
        }
    }
  }
  console.log(selections)
  if (totalSelected != 25){
    alert("NOT ALL GAMES SELECTED\nPlease make selections for games:\n"+notSelected)
  } else {
    alert("Thank you for making your selections")
  }
}
