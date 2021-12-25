$(function() {
	$('#article_list').text('Идёт загрузка списка статей');
	loadArticleList();
});

$('#save_article').click(function () {
    console.log('Сохранение статьи');
    saveAuthor();
});

function renderEditButton() {
    $('.edit_button').click(function (e) {
        console.log('Редактирование статьи');
        var el = e.target;
        var id = el.getAttribute('data-id');
        getArticle(id);
        console.log(id);
    });

    $('.delete_button').click(function (e) {
        console.log('Удаление статьи');
        var el = e.target;
        var id = el.getAttribute('data-id');
        deleteArticle(id);
        console.log(id);
    });

    $('#add_button').click(function () {
        console.log('Добваление статьи');
        getArticle(0);
        console.log("Объект: "+id);
    });
}

function loadArticleList()
{
    $.ajax({
        url: '/get_article_list',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data instanceof Array)
            {
				console.log("Успешная загрузка статей");
                renderArticleList(data);
            }
            else
            {
				console.log("Ошибка при загрузке статей");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg)
        }
    });
}

// Загрузка конкретного контакта
function getArticle(id)
{
    $.ajax({
        url: '/get_article',
        type: 'POST',
        dataType: 'json',
        // Запрос на данные об 1 статье по id
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Статья загружена");
                renderForm(data.user);
            }
            else
            {
                console.log("Ошибка при загрузке статьи");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

function deleteArticle(id)
{
    $.ajax({
        url: '/delete_article',
        type: 'POST',
        dataType: 'json',
        data: {
            id: id
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Статья удалена");
                loadArticleList();
            }
            else
            {
                console.log("Ошибка при удалении статьи");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: ' + errorMsg);
        }
    });
}

// Передача данных из формы на backend
function saveArticle()
{
    $.ajax({
        url: '/save_article',
        type: 'POST',
        dataType: 'json',
        data: {
            id: $('#id').val(),
            fio: $('#fio').val(),
            category: $('#category').val(),
            title: $('#title').val(),
            article: $('#article').val(),
            dt: $('#dt').val(),
        },
        success: function (data) {
            console.log(data);
            if (data.status == 'ok')
            {
                console.log("Статья сохранена");
                loadAuthorList();
                $('#article_form').hide();
            }
            else
            {
                console.log("Ошибка при сохранении статьи");
            }
        },
        error: function(jqxhr, status, errorMsg) {
            console.log('Ошибка при взаимодействии с сервером: '+errorMsg);
        }
    });
}

function renderArticleList(data)
{
    var html = '<p><button class="btn btn-primary" id="add_button">Добавить статью</button></p>';
    html += '<table class="table table-bordered small">';
    // Оформляем каждый элемент в виде строчки у таблицы
    data.forEach(function(item, i, data) {
        html += "<tr>";
        html += "<td>"+item['fio']+"</td>";
        html += "<td>"+item['category']+"</td>";
        html += "<td>"+item['title']+"</td>";
        html += "<td>"+item['article']+"</td>";
        html += "<td>"+item['dt']+"</td>";

        html += '<td><i class="bi bi-pencil-square edit_button" data-id="'+item['id']+'"></i></td>';
        html += '<td><i class="bi bi-trash delete_button" data-id="'+item['id']+'"></i></td>';
        html += "</tr>";
    });
    html += "</table>";

    $('#article_list').html(html);
    renderEditButton();
}

function renderForm(data) {
    $('#id').val(data['id']),
    $('#fio').val(data['fio']),
    $('#category').val(data['category']),
    $('#title').val(data['title']),
    $('#article').val(data['article']),
    $('#dt').val(data['dt']),

    $('#article_form').show();
}


