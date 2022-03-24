-- Создание таблицы авторов

CREATE TABLE `blog_authors` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`f` varchar(100) NOT NULL,
	`i` varchar(100) NOT NULL,
	`o` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);

-- Создание таблицы категорий

CREATE TABLE `blog_categories` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`category` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);

-- Создание таблицы статей

CREATE TABLE `blog_articles` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`category_id` INT NOT NULL,
	`author_id` INT NOT NULL,
	`title` varchar(100) NOT NULL,
	`article` TEXT NOT NULL,
	`dt` DATETIME NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `blog_articles` ADD CONSTRAINT `blog_articles_fk0` FOREIGN KEY (`category_id`) REFERENCES `blog_categories`(`id`);
ALTER TABLE `blog_articles` ADD CONSTRAINT `blog_articles_fk1` FOREIGN KEY (`author_id`) REFERENCES `blog_authors`(`id`);



-- Создание представления со всеми данными

CREATE OR REPLACE VIEW blog_articles_full AS SELECT
blog_articles.id, CONCAT_WS(' ', a.f, a.i, a.o) AS fio, c.category, blog_articles.title, blog_articles.article, blog_articles.dt
FROM blog_authors AS a, blog_categories AS c, blog_articles WHERE 
a.id = blog_articles.author_id AND c.id = blog_articles.category_id;

