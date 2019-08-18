var BASE_URL = "http://localhost:5000/";

function get_conn(target) {
    window.location.replace(BASE_URL + "get_connection/" + target);
}

function get_data(target, type) {
    window.location.replace(BASE_URL + "get_data/" + target + "/" + type);
}

function import_data(type) {
    window.location.replace(BASE_URL + "import_" + type);
}

function initiate_uploader() {
    var form = document.getElementById('file-form');
    var file = document.getElementById('file-select');
    var upload_button = document.getElementById('upload-button');

    file.onchange = function(event) {
        console.log(file.files);
        if(file.files[0].name === "records.csv") {
            upload_button.disabled = false;
        } else {

        }
    }

    form.onsubmit = function(event) {
        event.preventDefault();

        upload_button.innerHTML = 'Uploading..';

        var files = file.files;
        var form_data = new FormData();

        form_data.append('records', files[0], files[0].name);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', BASE_URL + 'upload_records', true);
        xhr.onload = function() {
            if(xhr.status === 200) {
                upload_button.innerHTML = 'Upload Complete';
            } else {
                alert("Error Occured in Upload");
            }
        };

        xhr.send(form_data);
    }
}
