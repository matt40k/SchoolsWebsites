CREATE TABLE IF NOT EXISTS school
(
	Urn int PRIMARY KEY ASC
	,LaCode int
	,LaName text
	,EstablishmentCode int
	,EstablishmentName text
	,TypeOfEstablishment text
	,SchoolWebsite text
	,Domain text
	,HeadName text
	,HeadJobTitle text
	,ModifiedDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
