# $Id$
CREATE TABLE IF NOT EXISTS version
(
        FileName                text            NOT NULL        PRIMARY KEY ASC
        ,Version		text            NOT NULL
        ,ModifiedDateTime       timestamp       NOT NULL        DEFAULT CURRENT_TIMESTAMP
);
