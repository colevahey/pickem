function login(){
  let username = document.getElementsByClassName("user")[0].value
  let password = document.getElementsByClassName("pass")[0].value
  console.log("Username:",username,"Password:",password)
  // IF USERNAME AND PASSWORD ARE VIABLE ACCOUNT
  let mainWindow = window.open("../index.html?uname="+username,"_blank","fullscreen=1")
}
