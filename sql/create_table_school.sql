CREATE TABLE IF NOT EXISTS school
(
	Urn			int		NOT NULL	PRIMARY KEY ASC
	,LaCode			int		NOT NULL
	,LaName			text		NOT NULL
	,EstablishmentCode	int		NOT NULL
	,EstablishmentName 	text		NOT NULL
	,TypeOfEstablishment 	text		NOT NULL
	,SchoolWebsite 		text		NOT NULL
	,Domain 		text		NOT NULL
	,HeadName 		text		NOT NULL
	,HeadJobTitle 		text		NOT NULL
	,ModifiedDateTime 	timestamp	NOT NULL	DEFAULT CURRENT_TIMESTAMP
);
