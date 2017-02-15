CREATE TABLE IF NOT EXISTS config
(
	Id			int		not null	PRIMARY KEY ASC
	,Name			text		not null
	,Value			text 		not null
	,ModifiedDateTime	timestamp	not null	DEFAULT CURRENT_TIMESTAMP
);
