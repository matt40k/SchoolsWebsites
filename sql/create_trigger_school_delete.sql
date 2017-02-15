CREATE TRIGGER IF NOT EXISTS trigger_school_delete
        AFTER DELETE
        ON school
BEGIN
	INSERT INTO audit(Urn, ChangeType, ChangeDesc, ModifiedDateTime) VALUES (new.Urn, "DELETE", "", datetime('now'));
END;
