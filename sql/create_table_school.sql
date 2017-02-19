CREATE TABLE IF NOT EXISTS school
(
	Urn			int		NOT NULL	PRIMARY KEY ASC
	,LaCode			int		NULL
	,LaName			text		NULL
	,EstablishmentCode	int		NULL
	,EstablishmentName 	text		NULL
	,TypeOfEstablishment 	text		NULL
	,SchoolWebsite 		text		NULL
	,Domain 		text		NULL
	,HeadName 		text		NULL
	,HeadJobTitle 		text		NOT NULL	DEFAULT 'Headteacher'
	,Ipv6Score		int		NULL
	,UKdomain		int		NULL
	,CMS			text		NULL
	,HTMLtype		text		NULL
	,HomepageSize		int		NULL
	,GoogleAnalytics	int		NULL
	,ModifiedDateTime 	timestamp	NOT NULL	DEFAULT CURRENT_TIMESTAMP
);
