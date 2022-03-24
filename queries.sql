-- Создание таблицы авторов

CREATE TABLE `blog_authors` (
  `id` int(11) NOT NULL,
  `f` varchar(100) NOT NULL,
  `i` varchar(100) NOT NULL,
  `o` varchar(100) NOT NULL
);


ALTER TABLE `blog_authors`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `blog_authors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

-- Создание таблицы категорий

CREATE TABLE `blog_categories` (
  `id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL
) ;


ALTER TABLE `blog_categories`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `blog_categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;



-- Создание таблицы статей

CREATE TABLE `blog_articles` (
  `id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `article` text NOT NULL,
  `dt` datetime NOT NULL
);


ALTER TABLE `blog_articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blog_articles_fk0` (`category_id`),
  ADD KEY `blog_articles_fk1` (`author_id`);


ALTER TABLE `blog_articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;


ALTER TABLE `blog_articles`
  ADD CONSTRAINT `blog_articles_fk0` FOREIGN KEY (`category_id`) REFERENCES `blog_categories` (`id`),
  ADD CONSTRAINT `blog_articles_fk1` FOREIGN KEY (`author_id`) REFERENCES `blog_authors` (`id`);



-- Создание представления со всеми данными

CREATE OR REPLACE VIEW blog_articles_full AS SELECT
blog_articles.id, CONCAT_WS(' ', a.f, a.i, a.o) AS fio, c.category, blog_articles.title, blog_articles.article, blog_articles.dt
FROM blog_authors AS a, blog_categories AS c, blog_articles WHERE 
a.id = blog_articles.author_id AND c.id = blog_articles.category_id;