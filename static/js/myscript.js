$(document).ready(function(){
    console.log("loaded");
//    $.material.init();

    $(document).on("submit", "#registerForm", function(e){
        e.preventDefault();
        console.log("form submitted");
        var form = $('#registerForm').serialize();
        $.ajax({
            url: '/postregistration',
            type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });

    $(document).on("submit", "#loginForm", function(e){
        e.preventDefault();
        var form = $(this).serialize();
        $.ajax({
            url: '/postUserLogin',
            type: 'POST',
            data: form,
            success: function(response){
                if(response == "error"){
                    alert("could not login..");
                }
                else{
                    console.log("logged in as", response);
                    window.location.href = '/'
                }
            }
        });
    });
    $(document).on("click", "#userLogout", function(e){
        e.preventDefault();
        $.ajax({
            url: '/logOut',
            type: 'GET',
            success: function(response){
                if(response == "success"){
                    alert('Successfully Logged Out :)')
                    window.location.href = '/'
                }
                else{
                    alert("Could'nt Log out...something went wrong :(" )
                }
            }
        });
    });
    $(document).on("submit", "#sharePostForm",function(e){
        e.preventDefault();
        var form = $('#sharePostForm').serialize();
        $.ajax({
            url: '/postPostsPosting',
            type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });

    $(document).on("submit", "#userInfoForm", function(e){
        e.preventDefault();
        var form = $(this).serialize();
        this.reset();
        $.ajax({
            url: '/generalSettingsInfo',
            type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });
});
function increaseLikes(num){
    var html = document.getElementById(num);
    html.innerHTML = parseInt(html.innerHTML) + 1;
    var form = {"num": num}
    $.ajax({
        url: '/updateLike',
        type: 'POST',
        data: form,
        success: function(response){
            console.log(response);
        }
    });
}

function doMeAFavour(count){
    var x = document.getElementById(count);
    if (x.style.display == "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function addComment(commentID){
    var form = $('#' + commentID).serialize();
    $.ajax({
        url: '/addCommentToPost',
        type: 'POST',
        data: form,
        success: function(response){
            console.log(response);
        }
    });
}