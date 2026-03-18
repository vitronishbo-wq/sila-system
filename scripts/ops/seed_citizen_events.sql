-- Seed portal events per citizen (idempotent).
-- Safe to run multiple times.
WITH citizens AS (
    SELECT
        id::text AS citizen_id,
        COALESCE(name, 'cidadão') AS name
    FROM citizenship_citizens
),
desired AS (
    SELECT
        c.citizen_id,
        'Boas-vindas ao SILA' AS title,
        ('Olá ' || c.name || ', o seu perfil foi ativado no SILA.') AS message,
        'portal' AS channel,
        (NOW() - interval '2 days') AS delivered_at
    FROM citizens c
    UNION ALL
    SELECT
        c.citizen_id,
        'Atualização de cadastro' AS title,
        ('O seu cadastro foi validado. Verifique os seus dados na FUC.') AS message,
        'portal' AS channel,
        (NOW() - interval '1 day') AS delivered_at
    FROM citizens c
),
inserted AS (
    INSERT INTO notifications (id, citizen_id, title, message, channel)
    SELECT
        gen_random_uuid(),
        d.citizen_id,
        d.title,
        d.message,
        d.channel
    FROM desired d
    WHERE NOT EXISTS (
        SELECT 1
        FROM notifications n
        WHERE n.citizen_id = d.citizen_id
          AND n.title = d.title
    )
    RETURNING id, title, channel
)
INSERT INTO notification_deliveries (id, notification_id, channel, status, delivered_at)
SELECT
    gen_random_uuid(),
    inserted.id,
    inserted.channel,
    'DELIVERED',
    CASE
        WHEN inserted.title = 'Boas-vindas ao SILA' THEN NOW() - interval '2 days'
        WHEN inserted.title = 'Atualização de cadastro' THEN NOW() - interval '1 day'
        ELSE NOW()
    END
FROM inserted;
