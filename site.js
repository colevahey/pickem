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
  user.style.float = "right"
  user.onclick = _ => openModal(username)
  navigationbar = document.querySelector("#navbar")
  navigationbar.appendChild(user)
}

const getDate = _ => {
  let gameDate = new Date()

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

const teamSet = (teamData, teamNode, gameNum) => {
  teamNode.className = teamData.homeAway
  teamNode.selected = false

  teamNode.onclick = _ => select(teamData.homeAway, gameNum)
    
  teamNode.onmouseover = e => {
    if (e.target.selected == false) {
      e.target.style = "background-color:#707070"
    }
    e.target.style.cursor = "pointer"
  }
  teamNode.onmouseout = e => {
    if (e.target.selected == false){
      e.target.style = "background-color:grey"
    }
    e.target.style.cursor = "default"
  }

  if (teamData.curatedRank.current < 99 && teamData.curatedRank.current != 0) {
    teamNode.innerHTML = "#" + teamData.curatedRank.current + " "
  } else {
    teamNode.innerHTML = ""
  }

  teamNode.innerHTML += teamData.team.displayName
  let teamClubhouse = document.createElement("a")
  teamClubhouse.href = teamData.team.links[0].href
  teamClubhouse.target = "_blank"
  let teamImage = document.createElement("img")
  teamImage.src = teamData.team.logo
  teamImage.height = "100"
  teamImage.style = "float:left;"
  teamClubhouse.appendChild(teamImage)
  teamNode.appendChild(teamClubhouse)

  return teamNode
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

    newGame.appendChild(teamSet(homeData, homeTeam, i))
    newGame.appendChild(spread)
    newGame.appendChild(teamSet(awayData, awayTeam, i))
    document.querySelector("#gamestable").appendChild(newGame)

  }
}

const select = (homeAway, teamNum) => {
  selectedTeam = document.getElementsByClassName(homeAway)[teamNum]
  partnerTeam = document.getElementsByClassName("homeaway".replace(homeAway,""))[teamNum]
  
  if (selectedTeam.selected == false) {
    selectedTeam.style = "background-color:#ff2d2d;"
    selectedTeam.selected = true
    partnerTeam.style = "background-color:grey;"
    partnerTeam.selected = false
  } else {
    selectedTeam.style = "background-color:grey;"
    selectedTeam.selected = false
  }
}

const finalCheck = gameDate => { 
  let games = document.querySelectorAll(".game")
  let totalSelected = 0
  let notSelected = "" 
  let selections = {"Username":document.querySelector("#username").innerHTML}
  selections[gameDate] = {}
  for (let i=0; i<games.length; i++) {
    let game = games[i]
    if (game.cells[0].selected) {
      console.log("Game",i+1,"home selected")
      totalSelected += 1
      selections[gameDate]["Game"+i] = "HOME"
    } else {
      if (game.cells[2].selected) {
        console.log("Game",i+1,"away selected")
        totalSelected += 1
        selections[gameDate]["Game"+i] = "AWAY"
      } else {
        console.log("NO TEAM SELECTED GAME",i+1)
        notSelected += i+1+" "
      }
    }
  }
  console.log(selections)
  if (totalSelected != 25){
    console.log("NOT ALL GAMES SELECTED\nPlease make selections for games:\n"+notSelected)
  } else {
    // Save the selections as a cookie
    console.log("Thank you for making your selections")
    cookieData = JSON.parse(document.cookie)
    cookieData["Username"] = selections["Username"]
    cookieData[gameDate] = selections[gameDate]
    document.cookie = JSON.stringify(cookieData)
  }
}

// For ease of testing
const homeSelectAll = _ => {
  let homeTeams = document.querySelectorAll('.home')
  homeTeams.forEach( node => node.click())
  finalCheck(getDate())
}

const openModal = username => {
  // Get the modal
  let modal = document.getElementById('myModal');
  
  // Get the <span> element that closes the modal
  let span = document.getElementsByClassName("close")[0];
  
  // When the user clicks the button, open the modal 
  modal.style.display = "block";
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = _ => modal.style.display = "none"
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = e => {
    if (e.target == modal) {
      modal.style.display = "none"
    }
  }

  // Read the cookie data
  if (JSON.parse(document.cookie)["Username"] == username){
    cookieObject = JSON.parse(document.cookie)
    gameDatesSaved = []
    for (key in cookieObject) {
      if (key != "Username"){
        console.log("Past selection date:", key)
        gameDatesSaved.push(key)
      } else {
        console.log("Username:", cookieObject[key])
      }
    }
    gameDatesSaved.forEach(gameDay => console.log(cookieObject[gameDay]))
    document.querySelector(".modal-body").innerHTML = gameDatesSaved
  }

}