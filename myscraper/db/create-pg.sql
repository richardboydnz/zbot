CREATE TABLE url_dim (
    url_id SERIAL PRIMARY KEY,
    url VARCHAR(1024) NOT NULL,
    protocol VARCHAR(10),
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    path TEXT,
    is_resource BOOLEAN,
    is_webpage BOOLEAN,
    resource_type VARCHAR(255),
    last_status_code INTEGER,
    file_extension VARCHAR(50),
    UNIQUE (url, domain_id)
);

CREATE TABLE link_fact (
    link_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    target_url_id INTEGER REFERENCES url_dim(url_id),
    content_id INTEGER REFERENCES content_dim(content_id),
    link_text TEXT,
    link_tag TEXT,
    link_attr TEXT,
    link_type TEXT,
    is_internal BOOLEAN
    UNIQUE (link_id)
);

CREATE TABLE html_dim (
    html_id SERIAL PRIMARY KEY,
    html_hash BIGINT,
    html_data TEXT NOT NULL,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    UNIQUE (html_hash, domain_id)
);

CREATE TABLE html_content_bridge (
    bridge_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    html_id INTEGER REFERENCES html_dim(html_id),
    content_id INTEGER,
    path TEXT NOT NULL,
    UNIQUE(domain_id, html_id, content_id)
);

CREATE TABLE download_fact (
    download_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),   -- Foreign key to domain_dim
    url_id INTEGER REFERENCES url_dim(url_id),            -- Foreign key to url_dim
    redirect_url_id INTEGER REFERENCES url_dim(url_id)
    html_id INTEGER,                                    -- New column for html_hash
    download_timestamp TIMESTAMP NOT NULL,                -- Timestamp of the download
    http_status INTEGER,                                  -- HTTP status code
    headers TEXT,                                         -- HTTP headers as text
    crawl_id INTEGER REFERENCES crawl_dim(crawl_id)       -- Foreign key to crawl_dim
    UNIQUE (crawl_id, url_id)
);

CREATE TABLE domain_dim (
    domain_id SERIAL PRIMARY KEY,
    domain_name VARCHAR(255) NOT NULL,
    UNIQUE (domain_name)
);

CREATE TABLE crawl_dim (
    crawl_id SERIAL PRIMARY KEY,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    crawl_timestamp TIMESTAMP,
    UNIQUE (domain_id, crawl_timestamp)
);

CREATE TABLE content_dim (
    content_id SERIAL PRIMARY KEY,
    content_hash BIGINT,
    content_text TEXT NOT NULL,
    content_type VARCHAR(50),
    plain_text TEXT,
    plain_hash BIGINT,
    domain_id INTEGER REFERENCES domain_dim(domain_id),
    fragment_hash BIGINT,
    fragment_text TEXT NOT NULL,
    UNIQUE (content_hash, domain_id)
);