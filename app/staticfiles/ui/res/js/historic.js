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

function makeRequest(url=base_url+"/api/historic/historic/all/") {
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
            drawTable(data["results"],true);
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

function drawTable(data,create_new) {
    let header = document.getElementById("headers")
    let body = document.getElementById("body")
    if(create_new){
      header.innerHTML = ""
    }
    body.innerHTML = ""
    // data = removeDuplicates(data, "vrn")
    
    if (data.length > 0) {
      if(create_new){
        let row = document.createElement("tr");
        for (let j = 0; j < Object.keys(data[0]).length; j++) {
            let th = document.createElement("th")
            th.innerHTML = Object.keys(data[0])[j].toUpperCase().replace(/_/g, " ");
            row.appendChild(th)
            // console.log()
        }
        header.appendChild(row)
        row = document.createElement("tr");
        for (let j = 0; j < Object.keys(data[0]).length; j++) {
            let th = document.createElement("th")
            let input = document.createElement("input")
            input.setAttribute("placeholder",Object.keys(data[0])[j].toUpperCase().replace(/_/g, " "))
            input.setAttribute("class",Object.keys(data[0])[j].replace(/ /g, "_"))
            input.addEventListener("change",search)
            th.appendChild(input)
            row.appendChild(th)
            // console.log()
        }
        //
        //
        
        // console.log(data[i]["vrn"])
        header.appendChild(row)
    }

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

function search(event){
  field = event.target
  $.ajax({
      url: base_url+'/api/historic/historic/all/?column_name='+field.classList[0].replace(/_/g," ")+"&search_query="+field.value,
      method: 'GET',
      headers:{
          'Authorization' : 'Bearer '+getToken()
      },
      async: true,
      dataType: 'json',
      success: function (data) {
          // console.log(data)
          // document.getElementById("prev-page").value = data["previous"]
          // document.getElementById("next-page").value = data["next"]
          drawTable(data["results"],false);
      },
      error: function (xhr, status, error) {
        if (xhr.status === 401) {
          refreshTokenRequest(makeRequest);
        } else {
          console.error(xhr.responseJSON);
        }
      }
    });
}

function filterDate(){
  start_date = document.getElementById("start-date").value
  end_date = document.getElementById("end-date").value
  makeRequest(base_url+'/api/historic/historic/all/?start_date='+start_date+"&end_date="+end_date)
}

function filterContent(){
  search = document.getElementById("search").value
  makeRequest(base_url+'/api/historic/historic/all/?search='+search)
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
