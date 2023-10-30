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
function login(object) {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var errorElem = document.getElementById("error");
    errorElem.innerHTML = ""
    var data = {
        email: email,
        password: password
    };

    $.ajax({
        url: base_url+'/api/user/token/',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            localStorage.setItem("access", data["access"]);
            localStorage.setItem("refresh", data["refresh"]);
            window.location.href = "historic.html";
        },
        error: function (xhr, status, error) {
            errorElem.innerHTML = xhr["responseJSON"]["detail"]
        }
    });
}
