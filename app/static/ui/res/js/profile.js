$(document).ready(function(){
    makeRequest()
    // setInterval(makeRequest, 2000);
});
function makeRequest() {
    $.ajax({
        type: 'GET',
        url: '/api/historic/CurrentUserView/',  // Your API endpoint
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
                async: true,
        dataType: 'json',
        success: function(response) {
            console.log(response);
            console.log(response.name);
            $('#username').text(response.name);  // Setting the user's name
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function setToken(newToken) {
  token = newToken;
}

function getToken() {
  return token;
}

function getRefreshToken() {
  return refreshToken;
}