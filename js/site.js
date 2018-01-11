function login(){
  uname = prompt("What is your username?")
  if (uname in {}){
    console.log("User found")
  } else {
    alert("User not found")
  }
}
