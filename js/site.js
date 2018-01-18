function login(){
  // For future use in a login page... For now we will leave
  // it here

  uname = document.getElementById("username").value
  pword = document.getElementById("password").value
  console.log(uname, pword)
}

function setgames(jsondata){

  for (i=0;i<jsondata.games.length;i++){
    game = jsondata.games[i]

    let newgame = document.createElement("tr")
    let awayteam = document.createElement("td")
    let hometeam = document.createElement("td")
    let spread = document.createElement("td")

    hometeam.className = "home"

    // FIX THIS
    hometeam.onclick = function(){select('home'+i)}

    hometeam.selected = false
    if (game.homeTeam.rank < 99) {
      hometeam.innerHTML = "#" + game.homeTeam.rank + " "
    } else {
      hometeam.innerHTML = ""
    }
    hometeam.innerHTML += game.homeTeam.displayName
    let homeimage = document.createElement("img")
    homeimage.src = game.homeTeam.logoUrl
    homeimage.height = "100"
    hometeam.appendChild(homeimage)

    spread.className = "versus"
    if (game.odds.spread != "N/A") {
      spread.innerHTML = game.odds.spread 
    } else {
      spread.innerHTML = game.scores.home + "  -  " + game.scores.away
    }

    awayteam.className = "away"

    // FIX THIS
    awayteam.onclick = function(){select("away"+i)}

    awayteam.selected = false
    if (game.awayTeam.rank < 99) {
      awayteam.innerHTML = "#" + game.awayTeam.rank + " "
    } else {
      awayteam.innerHTML = ""
    }
    awayteam.innerHTML += game.awayTeam.displayName 
    let awayimage = document.createElement("img")
    awayimage.src = game.awayTeam.logoUrl
    awayimage.height = "100"
    awayteam.appendChild(awayimage)

    newgame.appendChild(hometeam)
    newgame.appendChild(spread)
    newgame.appendChild(awayteam)
    document.getElementById("gamestable").appendChild(newgame)
  }
}

function select(teamnum){
  console.log("selecting", teamnum)  
}
