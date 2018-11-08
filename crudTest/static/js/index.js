var delay = 800;

function filter(e){
    var sender = e;

    clearTimeout(sender.data('timer'));

    sender.data('timer', setTimeout(function () {
        sender.removeData('timer');

        var query = location.search.substring(1).split('&');
        var parsedQuery = {};
        query.forEach(element => {
            var keyValue = element.split('=');
            parsedQuery[keyValue[0]] = keyValue[1];
        });
        delete parsedQuery['']

        var senderName = sender.attr('name');
        var newUrlParams = {};
        newUrlParams[senderName] = sender.val().replace(/\s/g, '');

        var queryKeys = ['name', 'text', 'date', 'limit', 'skip']
        queryKeys.forEach(function(key){
            if ((key in parsedQuery)&&(!(key in newUrlParams))) 
            { 
                newUrlParams[key] = parsedQuery[key]; 
            }
        });

        var newUrl ='?'
        for(key in newUrlParams)
        {
            if (newUrlParams[key].length>0)
                newUrl += key + '=' + newUrlParams[key] + '&'
        }
        newUrl = newUrl.slice(0, -1);
        window.location.replace(newUrl);
        
    }, delay));
};

function tableRowClick(row){
    var id = row.data("href");
    var url = new URL(window.location.href);
    url.searchParams.set('id', id)
    window.location.replace(url);
};

$("#table > tbody > tr").click(function(){
    tableRowClick($(this));
});

function getRequestArgumentValue(name){
    if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
       return decodeURIComponent(name[1]);
};

$(document).ready(function(){
    $('#recordOffset').val(getRequestArgumentValue('skip'));

    limit = getRequestArgumentValue('limit');
    if((typeof limit == 'undefined') || (limit == 0)) {
        $('#pages').addClass("disabledbutton")
        $('#rowsPerPage').val("0")
    }
    else {
        $('#rowsPerPage').val(limit)
    }
    
    id = getRequestArgumentValue('id');
    if (typeof id != 'undefined')
    {
        $.ajax({
            type: "GET",
            url: "/id/"+id,
            dataType: "json"
        }).done(function (data) {
            $("#formModal").modal();
            $.each(data, function (key, value) {
                if (key == '_id') name = key.replace('_', '')
                else name = key

                var input = document.getElementById('input' + name)
                if (input != null) {
                    input.value = value
                }
            });

            $('#delButton').show();
        });
    }

    drPickier.val('');

    var filterFieldsNames = ['name', 'text', 'date'];
    var parsedQuery = {};
    var flag = true;
    decodeURI(location.search.substring(1)).split('&').forEach(element => {
        var keyValue = element.split('=');
        var inputField =$('#filterForm input[name='+keyValue[0]+']');
        var val = keyValue[1].replace('-',' - ');
        if (inputField.length>0)
        {
            inputField.val(val);
            if(flag) { 
                flag = false;
                $('#filterFormCollapse').collapse('show');
            }
        }
    });
    
    delete parsedQuery['']

})

$('#rowsPerPage').click(function(){
    val = $(this).val();
    window.location.replace("/?limit="+val);
});

$('#delButton').click(function(){
    $('#formСonfirmation').show();
});

$('#btnDismiss').click(function(){
    $('#formСonfirmation').hide();
});

$('#btnСonfirm').click(function(){
    id = $('#inputid').val();
    $.get('/delete/' + id);
    window.location.replace('/');
});

$('#recordOffset').on('keyup change', function(){
    var sender = $(this);

    clearTimeout(sender.data('timer'));

    sender.data('timer', setTimeout(function () {
        sender.removeData('timer');

        var url = new URL(window.location.href);
        url.searchParams.set('skip', sender.val());
        window.location.replace(url);
    }, delay));
});