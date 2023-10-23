-- page table
CREATE TABLE page (
    pageId CHAR(64) PRIMARY KEY,  -- Assuming a 64-character hash
    domain VARCHAR(255) NOT NULL,
    initial_date TIMESTAMP NOT NULL,
    initial_source_url VARCHAR(2048) NOT NULL
);

-- url table
CREATE TABLE url (
    URL VARCHAR(2048) PRIMARY KEY,
    return_code SMALLINT NOT NULL,
    mime VARCHAR(255) NOT NULL,
    pageId CHAR(64) REFERENCES page(pageId),
    initial_referrer VARCHAR(2048),
    date_updated TIMESTAMP NOT NULL,
    protocol VARCHAR(10),  -- e.g., http, https
    subdomain VARCHAR(255),
    domain VARCHAR(255) NOT NULL,
    path VARCHAR(2048),
    query VARCHAR(2048),
    fragment VARCHAR(512),
    UNIQUE(protocol, subdomain, domain, path, query, fragment)  -- Combined unique key for URL components
);

-- link table
CREATE TABLE link (
    id SERIAL PRIMARY KEY,
    pageId CHAR(64) REFERENCES page(pageId),
    from_domain VARCHAR(255) NOT NULL,
    from_url VARCHAR(2048) NOT NULL,
    to_domain VARCHAR(255) NOT NULL,
    to_url VARCHAR(2048) NOT NULL
);

-- text table
CREATE TABLE text (
    pageId CHAR(64) PRIMARY KEY REFERENCES page(pageId),
    text_version TEXT NOT NULL
);

-- markdown table
CREATE TABLE markdown (
    pageId CHAR(64) PRIMARY KEY REFERENCES page(pageId),
    markdown_version TEXT NOT NULL
);
