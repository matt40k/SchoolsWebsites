CREATE TRIGGER IF NOT EXISTS trigger_school_insert
	AFTER INSERT
	ON school
BEGIN
	INSERT INTO audit(Urn, ChangeType, ChangeDesc, ModifiedDateTime) VALUES (new.Urn, "INSERT", "", datetime('now'));
END;
