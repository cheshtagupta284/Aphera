$(window).on('load', function () {
    $('#status').fadeOut();
    $('#preloader').delay(1000).fadeOut();

});
function generateHTML0(name, email, phone, status, id, types) {
    return `<div class="row">
    <div class="col-xl-12">
        <div class="card">
            <div class="row" data-store="${id}" data-types="${types}">
                <div class="col-md-10"><h4>My Requests</h4></div>
                <div class="col-md-1 button-hide accept"><button onclick="accept(this)" class="btn btn-success">Accept</button></div>                              
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card-head">
                        Request Posted By :
                    </div>
                    <h6 id="requester-name" class="field">${name}</h6>
                    <hr width="100%">
                </div>
                <div class="col-md-6">
                    <div class="card-head">
                        Email
                    </div>
                    <h6 id="requester-email" class="field">${email}</h6>
                    <hr width="100%">
                </div>
                
                <div class="col-md-6">
                    <div class="card-head">
                        Contact
                    </div>
                    <h6 id="requester-contact" class="field">${phone}</h6>
                    <hr width="100%">
                </div>
                <div class="col-md-6">
                    <div class="card-head">
                        Status
                    </div>
                    <h6 id="requester-status" class="field">${status}</h6>
                    <hr width="100%">
                </div>

            </div>
        </div>
    </div>
</div>`;
}

function generateHTML1(types, status) {
    return `<div>
        <span class="types">${types} </span>
        <span class="req-status">${status}</span>
    </div>`
}

function generateHTML2(name, email, phone, status, types, _id) {
    return `<div class="row">
    <div class="col-xl-12">
        <div class="card-inner">
            
            <div class="row" data-types="${types}" data-id="${_id}">
            <div class="col-md-10"><h4>${types}</h4></div>
            <div class="col-md-1 button-hide refresh"><button onclick="refresh(this)" class="btn btn-outline-secondary">Refresh</button></div>                              
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="card-head">
                        Request Posted To :
                    </div>
                    <h6 id="receiver-name" class="field">${name}</h6>
                    <hr width="100%">
                </div>
                <div class="col-md-6">
                    <div class="card-head">
                        Email
                    </div>
                    <h6 id="receiver-email" class="field">${email}</h6>
                    <hr width="100%">
                </div>

                <div class="col-md-6">
                    <div class="card-head">
                        Contact
                    </div>
                    <h6 id="receiver-contact" class="field">${phone}</h6>
                    <hr width="100%">
                </div>
                <div class="col-md-6">
                    <div class="card-head">
                        Status
                    </div>
                    <h6 id="receiver-status" class="field">${status}</h6>
                    <hr width="100%">
                </div>

            </div>
        </div>
    </div>
    
</div>
</div>`
}

function generateHTML3(types) {
    return `<div class = "row card-blood" style="margin-bottom: 20px;" data-types="${types}">
        <span class="types col-md-10">${types} </span>
        <span class="button-delete col-md-2"><button onclick="delete_blood(this)" class="btn btn-outline-danger">Delete</button></span>
    </div>`
}


$.ajax({
    type: 'GET',
    url: 'http://localhost:5000/user',
    success: r => {
        $("#store-name").append(r.user.stores[0].name);
        $("#registrar-name").replaceWith(r.user.name);
        $("#registrar-email").replaceWith(r.user.email);
        $("#registrar-contact").replaceWith(r.user.contact);
        $("#registrar-city").replaceWith(r.user.city);
        var req;
        for (req of r.user.requests) {
            console.log(req);
            $('#requests-received').append(generateHTML0(
                req.name,
                req.email,
                req.contact,
                req.status,
                req.store_id,
                req.types
            ));
            $('status-received-requests').append(generateHTML1(req.types, req.status));
            if (r.user.status == "accepted") {
                $("button").addClass("hide")
            }
        }
        var rec, s, blood;
        for (s of r.user.stores) {
            for (rec of s.requests) {
                console.log(rec)
                $('#requests-created').append(generateHTML2(
                    rec.receiver_name,
                    rec.receiver_mail,
                    rec.receiver_contact,
                    rec.status,
                    rec.types,
                    rec.id
                ));
            }
            for (blood of s.bloods) {
                $('#blood-created').append(generateHTML3(
                    blood.types
                ));
            }
        }


    },
    error: r => {
        console.log(r)
    },
    headers: {
        "Authorization": "Bearer " + localStorage.getItem('token')
    }
});

function accept(e) {

    var id = $(e.parentElement.parentElement).data('store');
    var types = $(e.parentElement.parentElement).data('types')
    var dat
    dat = {
        "status": "accepted",
        "types": types,
        "store_id": id
    }
    console.log(dat)
    $.ajax({
        type: 'PUT',
        url: 'http://localhost:5000/user/request',
        data: JSON.stringify(dat),
        success: (r) => {
            console.log(r)
            $(e.parentElement.parentElement).addClass("hide")
        },
        error: (r) => {
            console.log(r)
        },
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
}

$("#form-create-request").on('submit', (e) => {
    e.preventDefault();

    var types
    types = document.getElementById("types-select").value

    dat_store = {
        "types": types
    }

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/request',
        data: JSON.stringify(dat_store),
        success: (r) => {
            console.log(r)
        }
        , error: console.log,
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
});

function refresh(e) {

    var types = $(e.parentElement.parentElement).data('types')
    var _id = $(e.parentElement.parentElement).data('id')
    var dat
    dat = {
        "types": types,
        "_id": _id
    }
    console.log(dat)
    $.ajax({
        type: 'PUT',
        url: 'http://localhost:5000/request',
        data: JSON.stringify(dat),
        success: (r) => {
            console.log(r)
        },
        error: (r) => {
            console.log(r)
        },
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
}

$("#form-add-blood").on('submit', (e) => {
    e.preventDefault();

    var types
    types = document.getElementById("types-add-select").value

    dat_store = {
        "types": types
    }

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/blood',
        data: JSON.stringify(dat_store),
        success: (r) => {
            console.log(r)
        }
        , error: console.log,
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
});

function delete_blood(e) {
    var types = $(e.parentElement.parentElement).data('types')
    var dat
    dat = {
        "types": types,
    }
    console.log(dat)
    $.ajax({
        type: 'DELETE',
        url: 'http://localhost:5000/blood',
        data: JSON.stringify(dat),
        success: (r) => {
            console.log(r)
        },
        error: (r) => {
            console.log(r)
        },
        contentType: "application/json",
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        }
    });
}

$(".sign-out").click(function () {
    localStorage.clear();
    window.location.href = "/client/index.html"
})