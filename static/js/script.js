$("form textarea").on("keypress", function(e){
    if(e.which == 13){
        var txt = $("form textarea").val();
        var lines = txt.split("\n");
        var lastLine = lines[lines.length-1];

        if(lastLine.trim() !== "") {
            // Create a new radio button with the last line as its label
            var radioButton = $('<input type="radio" name="dynamicRadio" class="item-label">');
            var label = $('<label style="float: left;" class="item-label">').text(lastLine).prepend(radioButton);
            var delete_btn = $("<button style='background: transparent; border: none; display: fixed;'>").text("❌").on("click", function(){
                if($(this).siblings('label').find('input[type="radio"]').is(':checked')) {
                    // alert($(this).label());
                    $(this).closest('.label-container').remove();
                }
            });

            // Append the label (with radio button) to the container

            var label_container = $("<div class='label-container' style='float: left; width: 100%;'>").append(label).append(delete_btn).append('<br>');
            $("#radio-buttons-container").append(label_container);
        }
        // Clear the textarea
        $("form textarea").val('');
    }
})

$("#submit-button").on("click", function(){
    var txt = $("form textarea").val();
        var lines = txt.split("\n");
        var lastLine = lines[lines.length-1];

        if(lastLine.trim() !== "") {
            // Create a new radio button with the last line as its label
            var radioButton = $('<input type="radio" name="dynamicRadio" class="item-label">');
            var label = $('<label style="float: left;" class="item-label">').text(lastLine).prepend(radioButton);
            var delete_btn = $("<button style='background: transparent; border: none;'>").text("❌").on("click", function(){
                if($(this).siblings('label').find('input[type="radio"]').is(':checked')) {
                    // alert($(this).label());
                    $(this).closest('.label-container').remove();
                }
            });

            // Append the label (with radio button) to the container
            var label_container = $("<div class='label-container' style='float: left; width: 100%;'>").append(label).append(delete_btn).append('<br>');
            $("#radio-buttons-container").append(label_container);
            // alert($("#radio-buttons-container").text())
        }

        // Clear the textarea
        $("form textarea").val('');
})

$(".edit-button").on("click", function(){
     const finalItems = document.querySelectorAll('.final_item');

    // Create an array to hold the values
    const values = [];
    finalItems.forEach(item => {
        var lastLine = item.textContent
        if(lastLine.trim() !== "") {
            // Create a new radio button with the last line as its label
            var radioButton = $('<input type="radio" name="dynamicRadio" class="item-label">');
            var label = $('<label style="float: left;" class="item-label">').text(lastLine).prepend(radioButton);
            var delete_btn = $("<button style='background: transparent; border: none;'>").text("❌").on("click", function(){
                if($(this).siblings('label').find('input[type="radio"]').is(':checked')) {
                    // alert($(this).label());
                    $(this).closest('.label-container').remove();
                }
            });

            // Append the label (with radio button) to the container
            var label_container = $("<div class='label-container' style='float: left; width: 100%;'>").append(label).append(delete_btn).append('<br>');
            $(item).html(label_container)
            // alert($("#radio-buttons-container").text())
        }
    });

})

$(".update-button").on("click", function(){
    var main_title = $(".head-title").text()
    const all_items = []
    const data_dict = {}
    const radioButtons = $(".label-container");
    radioButtons.each(function(){
        const radioButton = $(this).find('label');
        const buttonValue = radioButton.text();
        all_items.push(buttonValue);
    })

    new_item = JSON.stringify({"members": all_items})

    Object.assign(data_dict, {
         "radioButtonValue": new_item,
         "title": main_title,
    })

    // Convert data_dict to JSON string
    const jsonBody = JSON.stringify(data_dict);

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    // Use fetch to send the POST request
    fetch('/update', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken,
        },
        body: jsonBody
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
        // Assuming the response redirects to '/home_page'
        window.location.href = '/home_page';
    })
    .catch(error => {
        console.error("Error: ", error);
    });

})

$(".create-button").on("click", function(){

    const form = $("#new_form")[0];
    const formData = new FormData(form);
    const all_items = []
    const date = $(".todate");
    const radioButtonContainer = $("#radio-button-container");
    const radioButtons = $('.label-container');
    radioButtons.each(function(){
        const radioButton = $(this).find('label');
        const buttonValue = radioButton.text();
        all_items.push(buttonValue);
    })
    formData.append('radioButtonValue', all_items);
    formData.append('date', date.text());


    fetch('/home_page', {
        method: "POST",
        body: formData
    }).then(response => response.text())
        .then(result => {
            console.log("Fetch result:", result);
            window.location.href = '/home_page';
        }).catch(error => {
            console.error("Error:", error);
        });
});

$(".remove-button").on("click", function(event){
    event.stopPropagation();
    const card_id = $(this).closest("div.card").data("todo-id");

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/delete_card', {
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken,
        },
        body: JSON.stringify({cardId: card_id})
    }).then(response => response.text())
      .then(result => {
            console.log("Fetch result:", result);
            window.location.href = "/home_page";
      }).catch(error => {
            console.error("Error:", error);
      });

});