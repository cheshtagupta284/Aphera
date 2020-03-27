
$("#Sign-in").on('submit', (e) => {
    e.preventDefault();
    data = $('#Sign-in').serializeArray()
    var user
    user = data[0].value
    var pass
    pass = data[1].value

    dat = { "email": user, "password": pass }
    console.log(dat)
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/login',
        data: JSON.stringify(dat),
        success: (r) => {
            localStorage.setItem('token', r['access_token']);
            window.location.href = 'pages/user_dash.html';
        },
        error: (r) => {
            window.location.href = "pages/error.html"
        },
        contentType: "application/json",
        dataType: 'json'
    });
});

$("#form-register-user").on('submit', (e) => {
    e.preventDefault();
    data = $('#form-register-user').serializeArray()
    var email
    email = data[0].value
    var pass
    pass = data[1].value
    var name
    name = data[2].value
    var city
    city = data[3].value
    var contact
    contact = parseInt(data[4].value)
    var age
    age = parseInt(document.getElementById("age-user").value);
    var types
    types = document.getElementById("type").value;

    dat = {
        "email": email,
        "name": name,
        "city": city,
        "role": "user",
        "contact": contact,
        "types": types,
        "age": age,
        "password": pass
    }
    console.log(dat)
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/register',
        data: JSON.stringify(dat),
        success: (r) => {
            console.log(r)
            window.location.href = '/index.html';
        }
        , error: console.log,
        contentType: "application/json",
        dataType: 'json'
    });
});

$("#form-register-registrar").on('submit', (e) => {
    e.preventDefault();
    data = $('#form-register-registrar').serializeArray()
    var email
    email = data[0].value
    var pass
    pass = data[1].value
    var name
    name = data[2].value
    var city
    city = data[3].value
    var contact
    contact = parseInt(data[4].value)

    dat_user = {
        "email": email,
        "name": name,
        "city": city,
        "role": "registrar",
        "contact": contact,
        "password": pass
    }

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/register',
        data: JSON.stringify(dat_user),
        success: (r) => {
            console.log(r)
        }
        , error: (r) => {
            console.log(r);
            window.location.href = "error.html"
        },
        contentType: "application/json",
        dataType: 'json'
    });

    dat = { "email": email, "password": pass }
    console.log(dat)
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/login',
        data: JSON.stringify(dat),
        success: (r) => {
            localStorage.setItem('token', r['access_token']);
            window.location.href = 'register_store.html';
        },
        error: (r) => {
            console.log(r)
        },
        contentType: "application/json",
        dataType: 'json'
    });
});

$("#form-register-store").on('submit', (e) => {
    e.preventDefault();
    data = $('#form-register-store').serializeArray()
    var city
    city = data[0].value
    var store_name1
    store_name1 = data[1].value
    var store_name2
    store_name2 = document.getElementById("types-select").value

    dat_store = {
        "name": store_name1.concat(store_name2),
        "city": city,
    }

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/store/register',
        data: JSON.stringify(dat_store),
        success: (r) => {
            console.log(r)
            window.location.href = 'store_dash.html'
        }
        , error: console.log,
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
});

$(".sign-out").click(function () {
    localStorage.clear();
    window.location.href = "/index.html"
})
