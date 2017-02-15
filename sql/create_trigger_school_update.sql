CREATE TRIGGER IF NOT EXISTS trigger_school_update
        AFTER UPDATE
        ON school
BEGIN
	INSERT INTO audit(Urn, ChangeType, ChangeDesc, ModifiedDateTime) VALUES (new.Urn, "UPDATE", "", datetime('now'));
END;
