
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
var listElm = document.querySelector('#infinite-list')
var nextPage = 0
var requestNext = true
var search_query = ""

$(document).ready(function () {
    makeRequest()
    // setInterval(makeRequest, 2000);
});


function makeRequest(url=base_url+"/api/riepilogo/riepilogo/") {
    document.getElementById("end-marker").innerHTML = ""
    var token = getToken();
    $.ajax({
        url: url,
        
        headers:{
            'Authorization' : 'Bearer '+ token
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            current_url = url
            nextPage = data["next"]
            console.log(data["next"])
            if(url.includes("page_no")){
                drawTable(data["results"],false,false);
            }else{
                drawTable(data["results"],true,false);
            }
            requestNext = true
        },
        error: function (xhr, status, error) {
          if (xhr.status === 401) {
            refreshTokenRequest(makeRequest);
          } else {
            console.error(error);
          }
        }
    });
        $.ajax({
        type: 'GET',
        url: '/api/historic/CurrentUserView/',  // Your API endpoint
        headers:{
            'Authorization' : 'Bearer '+ token
        },
                async: true,
        dataType: 'json',
        success: function(response) {
            $('#username, #username-, #user, #user-').text(response.name);
            $('#user-profile, #user-profilee, #user-profileee').attr('src', response.profile_image);


        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
    $.ajax({
        type: 'GET',
        url: '/api/historic/historic/total_counter/',  // Your API endpoint
        headers:{
            'Authorization' : 'Bearer '+ token
        },
                async: true,
        dataType: 'json',
        success: function(response) {
            $('#historic').text(response.all);
            $('#domestic_linehaul').text(response.domestic_linehaul);
            $('#retail_handling').text(response.retail_handling);
            $('#wholesale_distribution').text(response.wholesale_distribtion);
            $('#giacenze_vs_lgi').text(response.giacenze_vs_lgi);
                        $('#riepil').text(response.riepilogo);

        },
        error: function(error) {
            console.log('Error OF NEW:', error);
            console.error(error);
        }
    });
}

function drawTable(data,create_new_header,create_new_body) {
    let header = document.getElementById("headers")
    let body = document.getElementById("body")
    if(create_new_header){
        header.innerHTML = ""
    }
    if(create_new_body){
        body.innerHTML = ""
    }
    // data = removeDuplicates(data, "vrn")
    if (data.length > 0) {
        if(create_new_header){
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
                input.setAttribute("class",Object.keys(data[0])[j] + " form-control")

                if(Object.values(data[0])[j]['type'].includes("Date")){
                    input.setAttribute("type","Date")
                }
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
                let object = data[i][Object.keys(data[i])[j]]
                let td = document.createElement("td")
                config = {
                    parent : td,
                    content : object["value"],
                    editable : object["editable"],
                    class: Object.keys(data[i])[j]
                }
                if(object["type"].toLowerCase().includes("char")){
                    config['type'] = "text"
                }else if(object["type"].toLowerCase().includes("integer")){
                    config['type'] = "number"
                }else if(object["type"].toLowerCase().includes("datetime")){
                    config['type'] = 'datetime-local'
                }
                else if(object["type"].toLowerCase().includes("date")){
                    config['type'] = 'date'
                }else if(object["type"].toLowerCase().includes("time")){
                    config['type'] = 'time'
                }else if(object["type"].toLowerCase().includes("boolean")){
                    config['type'] = 'checkbox'
                }else if(object["type"].toLowerCase().includes("float")){
                    config['type'] = 'number'
                }else if(object["type"].toLowerCase().includes("double")){
                    config['type'] = 'number'
                }
                addChild(config['parent'],config['content'],config['editable'],config['type'],config['class'])
                row.appendChild(td)
            }
            body.appendChild(row)
        }
    }
}

function addChild(parent,content,editable,type,class_name){
    let input = document.createElement("input")
    if(!editable){
        input.setAttribute("disabled","")
        input.setAttribute("style","background:transparent; border:none;")
    }
    input.setAttribute("type",type)
    input.setAttribute("class",class_name)
    if(type === "checkbox"){
        input.setAttribute("checked","")
    }else{
        input.value = content
    }
    input.addEventListener("change",changed)
    parent.appendChild(input)
}

function changed(event){
    class_name = event.target.classList[0]
    value = event.target.value
    id = event.target.parentElement.parentElement.children[0].children[0].value

    payload = {
        [class_name]:value
    }
    $.ajax({
        url: base_url+'/api/riepilogo/riepilogo/'+id+'/',
        method: 'PATCH',
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
        data:payload,
        async: true,
        dataType: 'json',
        success: function (data) {
            console.log(data)
            // document.getElementById("prev-page").value = data["previous"]
            // document.getElementById("next-page").value = data["next"]
            // drawTable(data["results"]);
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

function search(event){
    document.getElementById("end-marker").innerHTML = ""
    field = event.target
    search_query = field.value
    $.ajax({
        url: base_url+'/api/riepilogo/riepilogo/?column_name='+field.classList[0]+"&search_query="+search_query,
        method: 'GET',
        headers:{
            'Authorization' : 'Bearer '+getToken()
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            console.log(data)
            nextPage = data["next"]
            // console.log(data)
            // document.getElementById("prev-page").value = data["previous"]
            // document.getElementById("next-page").value = data["next"]
            drawTable(data["results"],false,true);
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

function changePage(object){
    makeRequest(object.value)
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


listElm.addEventListener('wheel',function(){
    if(listElm.scrollTop + listElm.clientHeight >= listElm.scrollHeight-5){
        if(requestNext){
            if(nextPage != null){
                makeRequest(nextPage)
                requestNext = false
            }else{
                document.getElementById("end-marker").innerHTML = 'END'
            }
        }
    }
})