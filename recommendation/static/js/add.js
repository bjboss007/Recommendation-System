
function checkEmpty (){    var message = field_msg => ''+field_msg+' is required';
    if (($("#question").val()).length === 0){
        error = message('Question');
        $("#question-error").text(error)
    }else{
        $("#question-error").text("")
    }
    if (($("#answer").val()).length === 0){
        error = message('Answer');
        $("#answer-error").text(error)
    } else{
        $("#answer-error").text("")
    }
}

function removeItem(rowId){
    $(`#row-${rowId}-group`).remove()
}

$(document).ready(function (){
    count = 1
    var addButton = document.getElementById("addButton")
    var submitButton = document.getElementById("submit")
    submitButton.addEventListener("click", function(){
        checkEmpty()
    })
    
    addButton.addEventListener("click", function(){
        extra = `
                <div class = "form-group row" id = "row-${count}-group">
                    <input style = "margin-right:5px" type="text" name="option-${count}" id="option-${count}" class="form-control col-9"> 
                    <a style= "color : white" class = "btn btn-danger col-2" onClick = removeItem(${count})>-</a> 
                </div>    
            `
       $("#extra").append(extra)
       count+=1
    })
    
    
   
})


