
'use strict';

let ArrivalButton = document.getElementById('ArrivalButton');
let DepartureButton = document.getElementById('DepartureButton');
let NSInput = document.getElementById('NSInput');
let NSStations = document.getElementById('stations');

const URL_STATIONS = 'http://localhost:5000/stations/';
const URL_PLANNING_ARRIVAL = 'http://localhost:5000/route/arrival/';
const URL_PLANNING_DEPARTURE = 'http://localhost:5000/route/departure/';

let mode;

function fetchStations() {
    fetch(URL_STATIONS + NSInput.value)
      .then(data => {return data.json()})
      .then(res => {
        NSStations.innerHTML = '';
        res.locations.forEach((value) => {
          let li = document.createElement('li');
          li.innerHTML = value.name + "  " + value.type;
          li.className = 'item';
          li.id = value.id;

          NSStations.append(li);
        })
      })
}

DepartureButton.addEventListener("click", function () {
    fetchStations();
    mode = URL_PLANNING_DEPARTURE;
});

ArrivalButton.addEventListener("click", function () {
    fetchStations();
    mode = URL_PLANNING_ARRIVAL;
});

document.getElementById("stations").addEventListener("click",function(e) {
  if (e.target && e.target.matches("li.item")) {
    NSStations.innerHTML = '';

    fetch(mode + e.target.id)
        .then(data => {
          return data.json();
        })
        .then(res => {
            res.forEach((value) => {
                let li = document.createElement('li');
                li.innerHTML = value.kind + '<br> From: ' +
                    value.departure_location + '<br> To: ' +
                    value.arrival_location + '<br> Departure time: ' +
                    value.departure_time + '<br> Duration: ' +
                    value.duration + '<br> Arrival time: ' +
                    value.arrival_time;

                NSStations.append(li);
            });
        });
  }
});


