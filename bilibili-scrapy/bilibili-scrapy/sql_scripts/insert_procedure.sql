CREATE DEFINER=`root`@`%` PROCEDURE `insert_procedure`(IN id int(11),
								  name varchar(512),
								  av int(11),
								  author varchar(512),
								  plays int(11),
								  barrages int(11),
								  coins int(11),
								  update_time datetime,
								  update_time_short date,
								  category varchar(512),
								  favorites int(11),
								  replys int(11),
                  last_crawled date,
                  url varchar(512))
BEGIN
UPDATE `bilibili`.`video`
	SET
	`id` = id,
	`name` = name,
	`av` = av,
	`author` = author,
	`plays` = plays,
	`barrages` = barrages,
	`coins` = coins,
	`update_time` = update_time,
	`update_time_short` = update_time_short,
	`category` = category,
	`favorites` = favorites,
	`replys` = replys,
  `last_crawled` = last_crawled,
  `url` = url
	WHERE `bilibili`.`video`.`id` = id;
IF ROW_COUNT()=0 THEN
	INSERT INTO `bilibili`.`video`
		(`id`,
		`name`,
		`av`,
		`author`,
		`plays`,
		`barrages`,
		`coins`,
		`update_time`,
		`update_time_short`,
		`category`,
		`favorites`,
		`replys`,
    `last_crawled`,
    `url`)
		VALUES
			(id,
			name,
			av,
			author,
			plays,
			barrages,
			coins,
			update_time,
			update_time_short,
			category,
			favorites,
			replys,
      last_crawled,
      url);
END IF;
END