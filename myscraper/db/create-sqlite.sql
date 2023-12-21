
--- partition dim

CREATE TABLE domain_dim (
    domain_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_name TEXT NOT NULL,
    UNIQUE (domain_name)
);

--- dimensions

CREATE TABLE url_dim (
    url_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    protocol TEXT,
    domain_id INTEGER,
    path TEXT,
    is_resource BOOLEAN,
    is_webpage BOOLEAN,
    resource_type TEXT,
    last_status_code INTEGER,
    file_extension TEXT,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (url, domain_id)
);

CREATE TABLE html_dim (
    html_id INTEGER PRIMARY KEY AUTOINCREMENT,
    html_hash INTEGER,
    html_data TEXT NOT NULL,
    domain_id INTEGER,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (html_hash, domain_id)
);

CREATE TABLE crawl_dim (
    crawl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER,
    crawl_timestamp TEXT,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (domain_id, crawl_timestamp)
);

CREATE TABLE content_dim (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash INTEGER,
    content_text TEXT NOT NULL,
    content_type TEXT,
    plain_text TEXT,
    plain_hash INTEGER,
    domain_id INTEGER,
    fragment_hash INTEGER,
    fragment_text TEXT NOT NULL,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    UNIQUE (content_hash, domain_id)
);

--- facts

CREATE TABLE link_fact (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER,
    target_url_id INTEGER,
    content_id INTEGER,
    link_text TEXT,
    link_tag TEXT,
    link_attr TEXT,
    link_type TEXT,
    is_internal BOOLEAN,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    FOREIGN KEY(target_url_id) REFERENCES url_dim(url_id),
    FOREIGN KEY(content_id) REFERENCES content_dim(content_id),
    UNIQUE (link_id)
);

CREATE TABLE download_fact (
    download_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER,
    url_id INTEGER,
    redirect_url_id INTEGER,
    html_id INTEGER,
    download_timestamp TEXT NOT NULL,
    http_status INTEGER,
    headers TEXT,
    crawl_id INTEGER,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    FOREIGN KEY(url_id) REFERENCES url_dim(url_id),
    FOREIGN KEY(redirect_url_id) REFERENCES url_dim(url_id),
    FOREIGN KEY(html_id) REFERENCES html_dim(html_id),
    FOREIGN KEY(crawl_id) REFERENCES crawl_dim(crawl_id),
    UNIQUE (crawl_id, url_id)
);

CREATE TABLE html_content_bridge (
    bridge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER,
    html_id INTEGER,
    content_id INTEGER,
    path TEXT NOT NULL,
    FOREIGN KEY(domain_id) REFERENCES domain_dim(domain_id),
    FOREIGN KEY(html_id) REFERENCES html_dim(html_id),
    UNIQUE(domain_id, html_id, content_id)
);