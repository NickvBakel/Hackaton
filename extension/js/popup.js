
'use strict';

let NSButton = document.getElementById('NSButton');
let NSInput = document.getElementById('NSInput');
let NSStations = document.getElementById('stations');

const URL_STATIONS = 'http://localhost:5000/stations/';
const URL_PLANNING_ARRIVAL = 'http://localhost:5000/route/arrival/';
const URL_PLANNING_DEPARTURE = 'http://localhost:5000/route/departure/';

NSButton.addEventListener("click", function () {
  console.log('click');
  fetch(URL_STATIONS + NSInput.value)
      .then(data => {return data.json()})
      .then(res => {
        NSStations.innerHTML = '';
        res.locations.forEach((value) => {
          let li = document.createElement('li');
          li.innerHTML = value.name;
          li.className = 'item';
          li.id = value.id;

          NSStations.append(li);
        })
      })
});

document.getElementById("stations").addEventListener("click",function(e) {
  if (e.target && e.target.matches("li.item")) {
      chrome.extension.getBackgroundPage().console.log(e.target.id);
    fetch(URL_PLANNING_ARRIVAL + e.target.id)
        .then(data => {
          return data.json()
        })
        .then(res => {
          chrome.extension.getBackgroundPage().console.log(res);
        });
  }
});


