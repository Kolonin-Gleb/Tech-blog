$('#save_category').click(function () {
    console.log('Сохранение категории');
    saveCategory();
});

function renderEditButton() {
    $('.edit_button').click(function (e) {
        console.log('Редактирование категории');
        var el = e.target;
        var id = el.getAttribute('data-id');
        getCategory(id);
        console.log(id);
    });

    $('.delete_button').click(function (e) {
        console.log('Удаление категории');
        var el = e.target;
        var id = el.getAttribute('data-id');
        deleteCategory(id);
        console.log(id);
    });

    $('#add_button').click(function () {
        console.log('Добваление категории');
        getCategory(0);
        console.log("Объект: " + id);
    });
}

function loadCategoryList()
{
    $.ajax({
        url: '/get_category_list',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data instanceof Array) {
				console.log("Успешная загрузка категории");
                renderCategoryList(data);
            } else {
				console.log("Ошибка при загрузке категории");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log("Ошибка загрузке списка категорий: " + errorMsg)
        }
    });
}

function getCategory(id)
{
    $.ajax({
        url: '/get_category',
        type: 'POST',
        dataType: 'json',
        // Запрос на данные об 1 категории по id
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Категория загружена");
                renderForm(data.user);
            }
            else
            {
                console.log("Ошибка при загрузке категории");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

function deleteCategory(id)
{
    $.ajax({
        url: '/delete_category',
        type: 'POST',
        dataType: 'json',
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Категория удалена");
                loadCategoryList();
            }
            else
            {
                console.log("Ошибка при удалении категории");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

// Передача данных из формы на backend
function saveCategory()
{
    $.ajax({
        url: '/save_category',
        type: 'POST',
        dataType: 'json',
        // Взятие данных из формы по атрибуту id, упаковка их в data и отправка на url: '/save_author'
        data: {
            id: $('#id').val(),
            category: $('#category').val(),
        },
        // Обработка ответа на запрос return jsonify(out_data)
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Категория сохранена");
                loadCategoryList();
                $('#category_form').hide();
            }
            else
            {
                console.log("Ошибка при сохранении категории");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: '+errorMsg);
        }
    });
}

// Отображение списка авторов
function renderCategoryList(data)
{
    var html = '<p><button class="btn btn-primary" id="add_button">Добавить категорию</button></p>';
    html += '<table class="table table-bordered small">';
    // Оформляем каждый элемент в виде строчки у таблицы
    data.forEach(function(item, i, data) {
        html += "<tr>";
        html += "<td>"+item['name']+"</td>";
        html += '<td><i class="bi bi-pencil-square edit_button" data-id="'+item['id']+'"></i></td>';
        html += '<td><i class="bi bi-trash delete_button" data-id="'+item['id']+'"></i></td>';
        html += "</tr>";
    });
    html += "</table>";

    $('#category_list').html(html);
    renderEditButton();
}

function renderForm(data) {
    $('#id').val(data['id']),
    $('#category').val(data['category']),
    $('#category_form').show();
}

$(function() {
	$('#category_list').text('Идёт загрузка списка категорий');
	loadCategoryList();
});
