CREATE TABLE IF NOT EXISTS stagingEdubase
(
	Urn			int		NOT NULL	PRIMARY KEY ASC
	,LaCode			int		NULL
	,LaName			text		NULL
	,EstablishmentCode	int		NULL
	,EstablishmentName	text		NULL
	,TypeOfEstablishment	text		NULL
	,SchoolWebsite		text		NULL
	,Domain			text		NULL
	,HeadName		text		NULL
	,HeadJobTitle		text		NULL
	,ModifiedDateTime	timestamp	NOT NULL	DEFAULT CURRENT_TIMESTAMP
);
