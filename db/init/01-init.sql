\set ON_ERROR_STOP on

-- Create one role per microservice.
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'identity_user') THEN
        CREATE ROLE identity_user LOGIN PASSWORD 'identity_pass';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ops_user') THEN
        CREATE ROLE ops_user LOGIN PASSWORD 'ops_pass';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'billing_user') THEN
        CREATE ROLE billing_user LOGIN PASSWORD 'billing_pass';
    END IF;
END
$$;

-- Create one database per bounded context / service.
SELECT 'CREATE DATABASE db_identity OWNER identity_user'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'db_identity') \gexec

SELECT 'CREATE DATABASE db_parking_ops OWNER ops_user'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'db_parking_ops') \gexec

SELECT 'CREATE DATABASE db_billing OWNER billing_user'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'db_billing') \gexec

-- Lock down default schema permissions and grant each owner to its own db schema.
\connect db_identity
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO identity_user;

\connect db_parking_ops
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO ops_user;

\connect db_billing
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO billing_user;
