-- Normalize locations names to Title Case with Portuguese connectors in lowercase
-- Idempotent: running multiple times yields same results

BEGIN;

UPDATE locations
SET name = regexp_replace(
    regexp_replace(
        regexp_replace(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            initcap(regexp_replace(name, '-', ' - ', 'g')),
                            ' - ', '-', 'g'
                        ),
                        '(^|\s)E(\s|$)', '\1e\2', 'g'
                    ),
                    '(^|\s)De(\s|$)', '\1de\2', 'g'
                ),
                '(^|\s)Da(\s|$)', '\1da\2', 'g'
            ),
            '(^|\s)Do(\s|$)', '\1do\2', 'g'
        ),
        '(^|\s)Dos(\s|$)', '\1dos\2', 'g'
    ),
    '(^|\s)Das(\s|$)', '\1das\2', 'g'
);

COMMIT;
