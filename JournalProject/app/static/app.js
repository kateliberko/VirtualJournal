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

function dayofWeek(){
    var days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
    var d = new Date();
    var dayName = days[d.getDay()];
    var selectDiv = document.getElementById('dayheader');
    var todaycal = document.getElementById('day0');
    
    if (selectDiv){
        selectDiv.innerHTML = dayName;
    }
    if (todaycal){
        todaycal.innerHTML= dayName;
        var num = nextDay(d.getDay());
        
        document.getElementById('day1').innerHTML = days[num[0]];

        document.getElementById('day2').innerHTML = days[num[1]];

        document.getElementById('day3').innerHTML = days[num[2]];

        document.getElementById('day4').innerHTML = days[num[3]];

        document.getElementById('day5').innerHTML = days[num[4]];

        document.getElementById('day6').innerHTML = days[num[5]];
    }
    
    
}
function nextDay(num){
    if( num ==0){
        return[ 1, 2, 3, 4, 5, 6]
    }
    if( num ==1){
        return[  2, 3, 4, 5, 6, 0]
    }
    if( num ==2){
        return[ 3, 4, 5, 6, 1, 2]
    }
    if( num ==3){
        return[ 4, 5, 6, 0, 1, 2]
    }
    if( num ==4){
        return[ 5, 6, 0, 1, 2, 3]
    }
    if( num == 5){
        return[ 6, 0, 1, 2, 3, 4]
    }
    // if num == 6
    return[0, 1, 2, 3, 4, 5]
}

// https://stackoverflow.com/questions/49387685/create-a-vertical-line-that-overlays-all-html-content-and-moves-across-the-page/49387816

var vline=$('#vline');
setInterval(function(){
  vline.css('bottom', parseInt(vline.css('bottom')) + 1);
}, 50);

// var radios = document.getElementById["habitname"].elements["name of elements..?"];
//   for(radio in radios) {
//     radio.onclick = function() {
//         // habit function: should update Habit.habit_done with prooper boolean based on click
//     }
// }
// add function for onload:
// should check habits for habits with todays date (do they exist aleady?)
// if they exist, grab them and display their booleans correctly in habittracker table
// if they don't exist we need to grab current_user.habits and create habit for each (so they exist for todays date)