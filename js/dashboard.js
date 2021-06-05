$(window).on('load', function () {
    $('#status').fadeOut();
    $('#preloader').delay(1000).fadeOut();

});

function generateHTML(name, email, phone, status, id, types) {
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
</div>`
}

$.ajax({
    type: 'GET',
    url: 'http://localhost:5000/user',
    success: r => {
        if (r.user.role == 'registrar') {
            window.location.href = "store_dash.html"
        }
        $("#name-head").replaceWith(r.user.name);
        $("#name").replaceWith(r.user.name);
        $("#email").replaceWith(r.user.email);
        $("#contact").replaceWith(r.user.contact);
        $("#age").replaceWith(r.user.age);
        $("#types").replaceWith(r.user.types);
        $("#city").replaceWith(r.user.city);
        $("#status_user").replaceWith(r.user.status);
        var req;
        for (req of r.user.requests) {
            console.log(req);
            $('#requests').append(generateHTML(
                req.name,
                req.email,
                req.contact,
                req.status,
                req.store_id,
                req.types
            ));
            if (r.user.status == "accepted") {
                $(".accept").addClass("hide")
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

$(".sign-out").click(function () {
    localStorage.clear();
    window.location.href = "/index.html"
})