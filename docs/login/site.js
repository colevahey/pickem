function login(){
  let username = document.getElementsByClassName("user")[0].value
  let password = document.getElementsByClassName("pass")[0].value
  console.log("Username:",username,"Password:",password)
  let mainWindow = window.open("", "../index.html")
  mainWindow.document.username = username
  mainWindow.document.password = password
}
