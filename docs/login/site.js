function login(){
  let username = document.getElementsByClassName("user")[0].value
  let password = document.getElementsByClassName("pass")[0].value
  console.log("Username:",username,"Password:",password)
  let key = "01011010010"
  // IF USERNAME AND PASSWORD ARE VIABLE ACCOUNT
  // The key will be a universal key for the site
  let mainWindow = window.open("../index.html?uname="+username+"&key="+key,"_blank","fullscreen=1")
}
