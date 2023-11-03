var base_url = ''
fetch('file.txt')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.text();
  })
  .then(data => {
    // `data` contains the contents of the text file
    base_url = data
  })
  .catch(error => {
    console.error('Error:', error);
  });
$(document).ready(function () {
    list()
    // setInterval(makeRequest, 2000);
});

function download() {
    var id = document.getElementById("download-id").value;
    $.ajax({
        url: base_url+'/api/download/download_complete/?unique_id=' + id,
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        async: true,
        success: function(data) {
            document.getElementById("download-id").value = "";

            // Convert text data to Blob
            var blob = new Blob([data], { type: 'text/csv' });

            // Create a temporary URL for the Blob object
            var url = URL.createObjectURL(blob);

            // Create a temporary link and trigger the file download
            var link = document.createElement('a');
            link.href = url;
            link.download = 'generated_file.csv';
            link.click();

            // Clean up the temporary URL
            URL.revokeObjectURL(url);
        },
        error: function (xhr, status, error) {
          if (xhr.status === 401) {
            refreshTokenRequest(download);
          } else {
            console.error(error);
          }
        }
    });
}

function list(){
    $.ajax({
        url: base_url+'/api/download/',
        
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i<data.length;i++){
                document.getElementById("list").innerHTML += data[i]["unique_id"]+"<br>"
            }
        },
        error: function (xhr, status, error) {
        if (xhr.status === 401) {
            refreshTokenRequest(list);
        } else {
            console.error(error);
        }
        }
    });
}


let token = localStorage.getItem("access");
let refreshToken = localStorage.getItem("refresh");
function setToken(newToken) {
  token = newToken;
}

function getToken() {
  return token;
}

function getRefreshToken() {
  return refreshToken;
}


function refreshTokenRequest(request) {
    $.ajax({
      url: base_url+'/api/user/token/refresh/',
      method: 'POST',
      data: {
        'refresh': refreshToken
      },
      dataType: 'json',
      success: function (response) {
        const newAccessToken = response.access;
        localStorage.setItem("access", newAccessToken);
        setToken(newAccessToken)
        request()
      },
      error: function (xhr, status, error) {
          window.location.href = "login.html";
      }
    });
  }