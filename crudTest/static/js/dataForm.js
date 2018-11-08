$(document).ready(function () {
    $("#formModal").on('shown.bs.modal', function(e){
        $('#inputName').focus();
    });

    $('#formModal').on('hide.bs.modal', function () {
        document.getElementById("fform").reset();
        document.getElementById('inputid').value = '';
        document.getElementById("formErrorsContainer").style.display = "none";
        $('#delButton').hide();
        $('#formСonfirmation').hide();
    })

    $('#fform').on('submit', function (e) {
        e.preventDefault();

        var csrf_token = $('input[name="csrf_token"]').attr('value');

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            }
        });

        $.ajax({
            type: "POST",
            url: "/iu",
            data:  {
                id: $('#inputid').val(),
                name: $('#inputname').val(),
                text: $('#inputtext').val()
            },
            dataType: "json"
        }).done(function (data) {
            var container = document.getElementById("formErrorsContainer");
            var messageInfo = document.getElementById("formMessage");
            var messageErrors = document.getElementById("formErrors");
            messageErrors.innerHTML = '';

            if (Object.keys(data).length>0)
                if (!('result' in data))
                {
                    container.style.display = "block"
                    container.classList.add('alert-danger');
                    container.classList.remove('alert-success');

                    messageInfo.innerText = 'Помилки заповнення:'

                    var ul = document.createElement('ul');
                    var div = document.getElementById('formErrors');
                    div.innerHTML='';
                    div.appendChild(ul);

                    jQuery.each(data, function (field, error) {
                        var li = document.createElement('li');
                        li.innerText = error['fieldCaption']
                        var ul1 = document.createElement('ul');
                        li.appendChild(ul1)

                        ul.appendChild(li);
                        for (var i = 0; i < error['errors'].length; i++) {
                            var li1 = document.createElement('li');
                            li1.innerText = error['errors'][i]
                            ul1.appendChild(li1)
                        }
                    });
                }
                else {
                    container.style.display = "block"
                    messageInfo.innerText = 'Помилки відсутні'
                    container.classList.remove('alert-danger');
                    container.classList.add('alert-success');

                    function countdownTimer(callback)
                    {
                        setTimeout(function(){                        
                            callback()
                        }, 300);
                    };

                    countdownTimer(function(){
                        var url = new URL(window.location.href);
                        url.searchParams.delete('id')
                        window.location.replace(url);
                    });
                }
        });

    });
});