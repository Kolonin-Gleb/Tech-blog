$('#save_contact').click(function () {
    console.log('Сохранение автора');
    saveAuthor();
});

function renderEditButton() {
    $('.edit_button').click(function (e) {
        console.log('Редактирование автора');
        var el = e.target;
        var id = el.getAttribute('data-id');
        getAuthor(id);
        console.log(id);
    });

    $('.delete_button').click(function (e) {
        console.log('Удаление автора');
        var el = e.target;
        var id = el.getAttribute('data-id');
        deleteAuthor(id);
        console.log(id);
    });

    $('#add_button').click(function () {
        console.log('Добваление автора');
        getAuthor(0);
        console.log("Объект: "+id);
    });
}

function loadAuthorList()
{
    $.ajax({
        url: '/get_author_list',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data instanceof Array) {
				console.log("Успешная загрузка автора");
                renderAuthorList(data);
            } else {
				console.log("Ошибка при загрузке автора");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log("Ошибка загрузке списка авторов: " + errorMsg)
        }
    });
}

// Загрузка конкретного контакта
function getAuthor(id)
{
    $.ajax({
        url: '/get_author',
        type: 'POST',
        dataType: 'json',
        // Запрос на данные об 1 авторе по id
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Автор загружен");
                renderForm(data.user);
            }
            else
            {
                console.log("Ошибка при загрузке автора");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

function deleteAuthor(id)
{
    $.ajax({
        url: '/delete_contact',
        type: 'POST',
        dataType: 'json',
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Автор удален");
                loadAuthorList();
            }
            else
            {
                console.log("Ошибка при удалении автора");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

// Передача данных из формы на backend
function saveAuthor()
{
    $.ajax({
        url: '/save_author',
        type: 'POST',
        dataType: 'json',
        // Взятие данных из формы по атрибуту id, упаковка их в data и отправка на url: '/save_contact'
        data: {
            id: $('#id').val(),
            f: $('#f').val(),
            i: $('#i').val(),
            o: $('#o').val(),
        },
        // Обработка ответа на запрос return jsonify(out_data)
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Автор сохранен");
                loadAuthorList();
                $('#author_form').hide();
            }
            else
            {
                console.log("Ошибка при сохранении автора");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: '+errorMsg);
        }
    });
}

// Отображение списка контактов
function renderAuthorList(data)
{
    var html = '<p><button class="btn btn-primary" id="add_button">Добавить автора</button></p>';
    html += '<table class="table table-bordered small">';
    // Оформляем каждый элемент в виде строчки у таблицы
    data.forEach(function(item, i, data) {
        html += "<tr>";
        html += "<td>"+item['f']+"</td>";
        html += "<td>"+item['i']+"</td>";
        html += "<td>"+item['o']+"</td>";
        html += '<td><i class="bi bi-pencil-square edit_button" data-id="'+item['id']+'"></i></td>';
        html += '<td><i class="bi bi-trash delete_button" data-id="'+item['id']+'"></i></td>';
        html += "</tr>";
    });
    html += "</table>";

    $('#author_list').html(html);
    renderEditButton();
}

function renderForm(data) {
    $('#id').val(data['id']),
    $('#f').val(data['f']),
    $('#i').val(data['i']),
    $('#o').val(data['o']),

    $('#author_form').show();
}

$(function() {
	$('#author_list').text('Идёт загрузка списка авторов');
	loadAuthorList();
});
