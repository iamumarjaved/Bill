$(document).ready(function () {
    makeRequest()
    // setInterval(makeRequest, 2000);
});

function makeRequest(url="http://127.0.0.1/api/historic/historic/wholesale_distribtion/") {
        let urlObj = new URL(url);
    let currentPage = parseInt(urlObj.searchParams.get("page_no")) || 1
    var token = getToken();
    $.ajax({
        url: url,
        
            headers:{
                'Authorization' : 'Bearer '+ token
            },
        async: true,
        dataType: 'json',
        success: function (data) {
            drawTable(data["results"]);
            drawPaginationButtons(data, currentPage);

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
            cache: false,
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

function changePage(object) {
    let url = object.value;
    makeRequest(url);
}




function downloadRequest(object){
    object.innerHTML = "Requesting"
    $.ajax({
        url: 'http://127.0.0.1/api/historic/historic/download/',
        
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
  makeRequest('http://127.0.0.1/api/historic/historic/wholesale_distribtion/?start_date='+start_date+"&end_date="+end_date)
}

function filterContent(){
  search = document.getElementById("search").value
  makeRequest('http://127.0.0.1/api/historic/historic/wholesale_distribtion/?search='+search)
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
      url: 'http://127.0.0.1/api/user/token/refresh/',
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

function drawPaginationButtons(data, currentPage) {
    const container = $("#pagination-container");
    container.empty(); // Clear the current pagination buttons
    let totalPages = Math.ceil(data["count"] / 50); // Assuming 10 items per page

    if (data["previous"]) {
        container.append(`<button type="button" style="margin: 0.5%;" class="btn btn-light rounded-pill" value="${data["previous"]}" onclick="changePage(this)">&lt;</button>`);
    }

    // Calculate the range of pages to show
    let startPage = Math.max(currentPage - 2, 1);
    let endPage = Math.min(currentPage + 2, totalPages);

    if (currentPage <= 3) {
        endPage = Math.min(5, totalPages);
    } else if (currentPage > (totalPages - 3)) {
        startPage = totalPages - 4;
    }

    for (let i = startPage; i <= endPage; i++) {
    if (i === currentPage) {
        container.append(`<button type="button" style="margin: 0.5%;" class="btn btn-primary rounded-pill" value="http://127.0.0.1/api/historic/historic/wholesale_distribtion/?page_no=${i}" onclick="changePage(this)">${i}</button>`);
    } else {
        container.append(`<button type="button" style="margin: 0.5%;" class="btn btn-light rounded-pill" value="http://127.0.0.1/api/historic/historic/wholesale_distribtion/?page_no=${i}" onclick="changePage(this)">${i}</button>`);
    }
}


    // Show ellipsis if there are more pages lkafter the current visible range
    if (endPage < totalPages) {
        container.append(`<span class="mx-1">..</span>`);
    }

    if (data["next"]) {
        container.append(`<button type="button" style="margin: 0.5%;" class="btn btn-light rounded-pill" value="${data["next"]}" onclick="changePage(this)">&gt;</button>`);
    }
}

function handleInvoiceSearchInput(event) {
    console.log("function called");
    const invoiceNumber = event.target.value;
    if (invoiceNumber) {
        searchInvoiceByNumber(invoiceNumber);
    } else {
        // Optionally reset the table if the search input is empty
        makeRequest();
    }
}


function searchInvoiceByNumber(invoiceNumber) {
    const url = constructInvoiceSearchUrl(invoiceNumber);
    $.ajax({
        url: url,
        headers: {
            'Authorization': 'Bearer ' + getToken()
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            console.log(data,"data");
            drawTable(data["results"],true);
        drawPaginationButtons(data, currentPage);        },
        error: function(xhr, status, error) {
            if (xhr.status === 401) {
                refreshTokenRequest(makeRequest);
            } else {
                console.error(xhr.responseJSON);
            }
        }
    });
}

function constructInvoiceSearchUrl(invoiceNumber, base="http://127.0.0.1/api/historic/historic/invoice_search/?") {
    console.log(`${base}invoice_query=${invoiceNumber}`);
    return `${base}invoice_query=${invoiceNumber}`;
}
