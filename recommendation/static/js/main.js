$(document).ready(function (){
    var arm_select = document.getElementById('arms').value;
    // var subject_select = document.getElementsByTagName("tbody");
    var subject_select = document.getElementById("subjectRow")
    fetch('/register/' + arm_select).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            // console.table(data)
            for(const[index,subject] of data.subjects.entries()){
                console.log(index, subject)
                optionHTML += `<tr>
                                    <td>
                                        <input id="${subject.name}" class = "form-control" name="${subject.name}" required type="text" value="${subject.name}" disabled>
                                    </td>
                                    <td>
                                        <input id="${subject.name}-rating" class = "form-control" max="5" min="0" name="${subject.name}" type="number" value="" required>
                                    </td>
                                </tr>`;
            };
            subject_select.innerHTML = optionHTML;
        })
        
    });

});



var arm_select = document.getElementById('arms');
var subject_select = document.getElementById("subjectRow");

arm_select.onchange = function()  {
    arm = arm_select.value;
    // alert(arm)
    fetch('/register/' + arm).then(function(response) {
        response.json().then(function(data) {
            var optionHTML = '';
            console.table(data)
            for (const[index,subject] of data.subjects.entries()) {
                optionHTML += `<tr>
                <td>
                    <input id="${subject.name}" class = "form-control" name="${subject.name}" required type="text" value="${subject.name}" disabled>
                </td>
                <td>
                    <input id="${subject.name}-rating" class = "form-control" max="5" min="0" name="${subject.name}" type="number" value="" required>
                </td>
            </tr>`;
            }
            subject_select.innerHTML = optionHTML;
        })
        
    });
};

