document.addEventListener('DOMContentLoaded', function (event) {
  document.getElementById('footerText').innerHTML += new Date().getFullYear()
  setGreetingByTime()
})

function sendData () {
  const navigatorData = {
    language: navigator.language,
    userAgent: navigator.userAgent,
    osCpu: navigator.oscpu
  }
  fetch('/collect-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ event: 'page_view', navigator: navigatorData })
  })
}
sendData()

function setGreetingByTime () {
  const curHours = new Date().getHours()
  const mainHeader = document.getElementById('main-header')
  if (curHours >= 0 && curHours < 5) {
    mainHeader.innerHTML = 'Good night!'
  } else if (curHours >= 5 && curHours < 12) {
    mainHeader.innerHTML = 'Good morning!'
  } else if (curHours >= 12 && curHours < 18) {
    mainHeader.innerHTML = 'Good afternoon!'
  } else if (curHours >= 18) {
    mainHeader.innerHTML = 'Good evening!'
  }
}
