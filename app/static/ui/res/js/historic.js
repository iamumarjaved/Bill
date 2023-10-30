$(document).ready(function () {
    makeRequest();

    // setInterval(makeRequest, 2000);
});

let activeFilters = {
    dateType: "",
    fromDate: "",
    toDate: "",
    country: "",
    shpStatus: "",
    brand: "",
    customerType: "",
    documentCode: "",
    documentType: "",
    type_type: "",
    invoiceNumber: ""
};


function makeRequest(url="http://127.0.0.1/api/historic/historic/all/") {
        let urlObj = new URL(url);
    let currentPage = parseInt(urlObj.searchParams.get("page_no")) || 1
    var token = getToken();
    $.ajax({
        url: url,

        headers:{
            'Authorization' : 'Bearer '+token
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            drawTable(data["results"],true);
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

function drawTable(data,create_new) {
    let header = document.getElementById("headers")
    let body = document.getElementById("body")
    if(create_new){
      header.innerHTML = ""
    }
    body.innerHTML = ""
    // data = removeDuplicates(data, "vrn")
    console.log(data, "func");
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
            input.setAttribute("class",Object.keys(data[0])[j].replace(/ /g, "_") + " form-control")
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
                let td = document.createElement("td");
                if (Object.keys(data[i])[j] === 'Invoice #') {  // replace 'invoice_number' with the actual key name in your data

                    let a = document.createElement('a');
                    a.href = `/api/historic/invoice/${data[i]['Invoice #']}/`;
                    a.target = '_blank'; // to open in a new tab
                    a.innerHTML = data[i][Object.keys(data[i])[j]];
                    td.appendChild(a);
                } else {
                    td.innerHTML = data[i][Object.keys(data[i])[j]];
                }

                row.appendChild(td);
            }
            body.appendChild(row);
        }

    }

}

// function changePage(object){
//     makeRequest(object.value)
// }

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
    console.log('http://127.0.0.1/api/historic/historic/all/?column_name='+field.classList[0].replace(/_/g," ")+"&search_query="+field.value);
  $.ajax({
      url: 'http://127.0.0.1/api/historic/historic/all/?column_name='+field.classList[0].replace(/_/g," ")+"&search_query="+field.value,
      method: 'GET',
      headers:{
          'Authorization' : 'Bearer '+getToken()
      },
      async: true,
      dataType: 'json',
      success: function (data) {
            drawTable(data["results"],true);
                    drawTable(data["results"]);
        drawPaginationButtons(data, currentPage);
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
  makeRequest('http://127.0.0.1/api/historic/historic/all/?start_date='+start_date+"&end_date="+end_date)
}

function filterContent(){
  search = document.getElementById("search").value
  makeRequest('http://127.0.0.1/api/historic/historic/all/?search='+search)
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

function applyFilters() {
    // Gather filter data
    activeFilters.dateType = document.getElementById("dateType").value;
    activeFilters.fromDate = document.getElementById("fromDate").value;
    activeFilters.toDate = document.getElementById("toDate").value;
    activeFilters.country = document.getElementById("country").value;
    activeFilters.shpStatus = document.getElementById("shpStatus").value;
    activeFilters.brand = document.getElementById("brand").value;
    activeFilters.customerType = document.getElementById("customerType").value;
    activeFilters.documentCode = document.getElementById("customer_code").value;
    activeFilters.documentType = document.getElementById("documentType").value;
    activeFilters.type_type = document.getElementById("type_type").value;
    activeFilters.invoiceNumber = document.getElementById("invoice-filter").value;


    // Construct the filter URL
    let filterUrl = constructFilterUrl();

    // Request data using the filters
    makeRequestt(filterUrl);
    toggleFilterPopup();
}

function constructFilterUrl(base="http://127.0.0.1/api/historic/historic/all/?") {
    let filterUrl = base;

    const databaseKeyMapping = {
        dateType: "date_type",
        fromDate: "start_date",
        toDate: "end_date",
        country: "country",
        shpStatus: "Shp_status",
        brand: "Brand",
        customerType: "customer_type", // Assuming this is correct
        documentCode: "customer_code", // Assuming this is correct
        documentType: "document_type",  // Assuming this is correct
        type_type: "type_type",  // Assuming this is correct
        invoiceNumber: "invoice"
    };

    for (const [key, value] of Object.entries(activeFilters)) {
        if (value) {
            const databaseKey = databaseKeyMapping[key];
            if (databaseKey === "document_type") {
                filterUrl += `${value}=${activeFilters.type_type}&`;
                break;
            } else {
                filterUrl += `${databaseKey}=${value}&`;
            }
        }
    }

    return filterUrl;
}


function changePage(object) {
    let url = object.value;
    makeRequest(url);
}



function makeRequestt(url) {
    var token = getToken();
    $.ajax({
        url: url,

        headers:{
            'Authorization' : 'Bearer '+token
        },
        async: true,
        dataType: 'json',
        success: function (data) {
            drawTable(data["results"],true);
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


