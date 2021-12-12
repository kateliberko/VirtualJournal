

function dayofWeek(){
    var daysabrv = ['SUN', 'MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT'];
    var days = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
    var d = new Date();
    var dayNameabrv = daysabrv[d.getDay()];
    var dayName = days[d.getDay()];
    var selectDiv = document.getElementById('dayheader');
    var todaycal = document.getElementById('day0');
    
    if (selectDiv){
        selectDiv.innerHTML = dayName;
    }
        todaycal.innerHTML= dayNameabrv;
        var num = prevDay(d.getDay());
        
        document.getElementById('day1').innerHTML = daysabrv[num[5]];

        document.getElementById('day2').innerHTML = daysabrv[num[4]];

        document.getElementById('day3').innerHTML = daysabrv[num[3]];

        document.getElementById('day4').innerHTML = daysabrv[num[2]];

        document.getElementById('day5').innerHTML = daysabrv[num[1]];

        document.getElementById('day6').innerHTML = daysabrv[num[0]];
    
    
}
function prevDay(num){
    if( num ==0){
        return[ 1, 2, 3, 4, 5, 6]
    }
    if( num ==1){
        return[ 2, 3, 4, 5, 6, 0]
    }
    if( num ==2){
        return[ 3, 4, 5, 6, 0, 1]
    }
    if( num ==3){
        return[ 4, 5, 6, 0, 1, 2]
    }
    if( num ==4){
        return[5, 6, 0, 1, 2, 3]
    }
    if( num == 5){
        return[ 6, 0, 1, 2, 3, 4]
    }
    // if num == 6
    return[0, 1, 2, 3, 4, 5]
}

// https://stackoverflow.com/questions/29943/how-to-submit-a-form-when-the-return-key-is-pressed
function checkSubmit(e) {
    if(e && e.keyCode == 13) {
       document.forms[0].submit();
    }
 }

