// Kate Liberko

class EventItem { // Event Creation
    constructor(name, location, day, startTime, endTime, duration) {
        this.name = name;
        this.location = location;
        this.day = day;
        this.startTime = startTime;
        this.endTime = endTime;
        this.duration = duration;
    }
}

function createEvent(name, location, start, end, startHeight, endHeight) { // create a div element with a class name "event-item" that contains the event's info from form
    newEvent = document.createElement('div');
    newEvent.setAttribute("class", "event-item");

    height = Number(endHeight / 2.85) - Number(startHeight / 2.85); // divide by 2.85 so 11:45pm meets end of calendar
    if (height <= 0) {
        alert("Start time must be before end time!");       // alert client of user error
    }

    newEvent.setAttribute("style", "top:" + startHeight / 2.85 + "px;height:" + height + "px;");
    strong = document.createElement('strong');
    br = document.createElement('br');
    br2 = document.createElement('br');
    strong.append(name);
    location = document.createTextNode(location);
    time = document.createTextNode(start + " to " + end);
    newEvent.append(strong);
    newEvent.append(br);
    newEvent.append(location);
    newEvent.append(br2);
    newEvent.append(time);
    return newEvent;
}

function placeEvent(dayInput, name, location, start, end, startVal, endVal) { // render event to the appropriate day column on your schedule
    var text = document.querySelectorAll('.title');
    for (i = 0; i < text.length; i++) {
        var innerText = text[i].innerHTML;
        if (innerText.toLowerCase() === dayInput) {  // check input day  against existing day columns
            var createdEvent = createEvent(name, location, start, end, startVal, endVal);
            var selectDiv = document.querySelectorAll('.content')[i];
            selectDiv.innerHTML = createdEvent.outerHTML; // place created event into corrent day div
        }

    }
}

var showingForm = false; // keeps track of form being shown or hidden

function showForm() {
    document.getElementById("add_event_form").style.display = 'block';
    showingForm = true;
}
function hideForm() {
    document.getElementById("add_event_form").style.display = 'none';
    showingForm = false;
}

function toggleForm() { // this will open the form for a new entry, and close the form once submitted
    showingForm ? hideForm() : showForm();
}


function makeTime(selector) { // modeled after Li0liQ's posting on StackOverflow- https://stackoverflow.com/questions/8918168/javascript-dynamic-time-drop-down
    var hours, minutes, meridiem;               //this function creates 15 min interval times from 12:00AM to 11:45pm to fill the start/end time options
    for (var i = 0; i <= 1425; i += 15) {
        hours = Math.floor(i / 60);
        minutes = i % 60;
        if (minutes < 10) {
            minutes = '0' + minutes; // adding leading zero
        }
        meridiem = hours % 24 < 12 ? 'AM' : 'PM';
        hours = hours % 12;
        if (hours === 0) {
            hours = 12;
        }

        starting = document.createElement('option');
        document.getElementById(selector).append(starting);
        starting.setAttribute('value', i);
        starting.append(hours + ':' + minutes + ' ' + meridiem);
    }
}

makeTime('endtime');
makeTime('starttime');

function addNewEvent() { // get form results and pass them to be formatted and placed on the correct day and time
    var event = new EventItem;
    event.name = document.getElementById("name").value;

    event.location = document.getElementById("location").value;

    var selectDay = document.getElementById("dayofweek");
    event.day = selectDay.options[selectDay.selectedIndex].value;

    var selectStartTime = document.getElementById("starttime");
    event.startTime = selectStartTime.options[selectStartTime.selectedIndex].innerHTML;

    var selectEndTime = document.getElementById("endtime");
    event.endTime = selectEndTime.options[selectEndTime.selectedIndex].innerHTML;

    var findStartValue = document.getElementById("starttime");
    event.findStartValue = findStartValue.options[findStartValue.selectedIndex].value; // get start time value for event placement

    var findEndValue = document.getElementById("endtime");
    event.findEndValue = findEndValue.options[findEndValue.selectedIndex].value; // get end time value for event placement
    console.log(event.findEndValue + "this is starting number");

    placeEvent(event.day, event.name, event.location, event.startTime, event.endTime, event.findStartValue, event.findEndValue);

}
