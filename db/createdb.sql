-- Drop tables in reverse order to avoid foreign key constraints issues
DROP TABLE IF EXISTS html_content_bridge;
DROP TABLE IF EXISTS link_fact;
DROP TABLE IF EXISTS download_fact;
DROP TABLE IF EXISTS content_dim;
DROP TABLE IF EXISTS html_dim;
DROP TABLE IF EXISTS domain_dim;
DROP TABLE IF EXISTS url_dim;
DROP TABLE IF EXISTS crawl_dim;

-- Implicit Dimension Tables
-- used anywhere

CREATE TABLE crawl_dim (
    crawl_id SERIAL PRIMARY KEY,
    crawl_hash BIGINT,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    crawl_timestamp TIMESTAMP,
    UNIQUE (crawl_hash, domain_id)
);

CREATE TABLE domain_dim (
    domain_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL,
);

CREATE TABLE url_dim (
    url_id SERIAL PRIMARY KEY,
    url VARCHAR(1024) NOT NULL,
    protocol VARCHAR(10),
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    path TEXT,
    UNIQUE (url_hash, domain_id)
);

-- Explicit Dimension Tables

-- html dim used for download
CREATE TABLE html_dim (
    html_id SERIAL PRIMARY KEY,
    html_hash BIGINT,
    html_data TEXT NOT NULL,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    UNIQUE (html_hash, domain_id)
);

-- content dim used for link
CREATE TABLE content_dim (
    content_id SERIAL PRIMARY KEY,
    content_hash BIGINT,
    content_text TEXT NOT NULL, -- This field was missing and has been added
    content_type VARCHAR(50) CHECK (content_type IN ('page', 'header', 'footer', 'aside', 'nav')),
    plain_text TEXT,
    plain_text_hash BIGINT,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    UNIQUE (content_hash, domain_id)
);

-- Fact Tables

-- Downloads Fact Table
CREATE TABLE download_fact (
    download_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),   -- Foreign key to domain_dim
    url_id INTEGER REFERENCES url_dim(url_id),            -- Foreign key to url_dim
    html_id INTEGER,                                    -- New column for html_hash
    download_timestamp TIMESTAMP NOT NULL,                -- Timestamp of the download
    http_status INTEGER,                                  -- HTTP status code
    headers TEXT,                                         -- HTTP headers as text
    crawl_id INTEGER REFERENCES crawl_dim(crawl_id)       -- Foreign key to crawl_dim
);


-- Links Fact Table
CREATE TABLE link_fact (
    link_id SERIAL PRIMARY KEY,
    fragment_id INTEGER REFERENCES content_dim(content_id),
    target_url_id INTEGER REFERENCES url_dim(url_id),
    link_text TEXT,
    crawl_id INTEGER REFERENCES crawl_dim(crawl_id),
    domain_id INTEGER REFERENCES domain_dim(domain_id)
);

-- Additional Table for HTML-Content Association
CREATE TABLE html_content_bridge (
    html_id INTEGER REFERENCES html_dim(html_id),
    content_id INTEGER REFERENCES content_dim(content_id),
    content_path TEXT,
    PRIMARY KEY (html_id, content_id)
);
