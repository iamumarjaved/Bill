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
    makeRequest()
    // setInterval(makeRequest, 2000);
});

function makeRequest(url=base_url+"/api/historic/historic/retail_handling/") {
    $.ajax({
        url: url,
        
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            console.log(data["count"])
            document.getElementById("prev-page").value = data["previous"]
            document.getElementById("next-page").value = data["next"]
            drawTable(data["results"]);
        },
        error: function (xhr, status, error) {
          if (xhr.status === 401) {
            refreshTokenRequest(makeRequest);
          } else {
            console.error(error);
          }
        }
    });
}

function drawTable(data) {
    let header = document.getElementById("headers")
    let body = document.getElementById("body")
    header.innerHTML = ""
    body.innerHTML = ""
    // data = removeDuplicates(data, "vrn")
    let row = document.createElement("tr");
    if (data.length > 0) {
        for (let j = 0; j < Object.keys(data[0]).length; j++) {
            let th = document.createElement("th")
            th.innerHTML = Object.keys(data[0])[j].toUpperCase()
            row.appendChild(th)
            // console.log()
        }
        //
        //
        
        // console.log(data[i]["vrn"])
        header.appendChild(row)

        for (let i = 0; i < Object.values(data).length; i++) {
            let row = document.createElement("tr");
            for (let j = 0; j < Object.keys(data[i]).length; j++) {
                let td = document.createElement("td")
                td.innerHTML = data[i][Object.keys(data[i])[j]]
                row.appendChild(td)
                // console.log()
            }
            // console.log(data[i]["vrn"])
            body.appendChild(row)
        }
    }
}

function changePage(object){
    makeRequest(object.value)
}

function downloadRequest(object){
    object.innerHTML = "Requesting"
    $.ajax({
        url: base_url+'/api/historic/historic/download/',
        
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            console.log(data)
            object.innerHTML = "Download Request"
        },
        error: function (xhr, status, error) {
          if (xhr.status === 401) {
            refreshTokenRequest(downloadRequest);
          } else {
            console.error(error);
          }
        }
    });
}

function filterDate(){
  start_date = document.getElementById("start-date").value
  end_date = document.getElementById("end-date").value
  makeRequest(base_url+'/api/historic/historic/retail_handling/?start_date='+start_date+"&end_date="+end_date)
}

function filterContent(){
  search = document.getElementById("search").value
  makeRequest(base_url+'/api/historic/historic/retail_handling/?search='+search)
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
