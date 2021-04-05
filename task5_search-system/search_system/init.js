const fs = require('fs')
const path = require('path')
const sanitizeHtml = require("sanitize-html");
const axios = require('axios');
const { Client } = require('pg')

/*
* config = {
  user?: string, // default process.env.PGUSER || process.env.USER
  password?: string, //default process.env.PGPASSWORD
  host?: string, // default process.env.PGHOST
  database?: string, // default process.env.PGDATABASE || process.env.USER
  port?: number, // default process.env.PGPORT
  connectionString?: string, // e.g. postgres://user:password@host:5432/database
  ssl?: any, // passed directly to node.TLSSocket, supports all tls.connect options
  types?: any, // custom type parsers
  statement_timeout?: number, // number of milliseconds before a statement in query will time out, default is no timeout
  query_timeout?: number, // number of milliseconds before a query call will timeout, default is no timeout
  connectionTimeoutMillis?: number, // number of milliseconds to wait for connection, default is no timeout
  idle_in_transaction_session_timeout?: number // number of milliseconds before terminating any session with an open idle transaction, default is no timeout
}
* */

const client = new Client({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'postgres',
    database: 'infosearch'
});
const linksText = fs.readFileSync('./links.txt', { encoding: 'UTF-8' });
const links = linksText.split('\n');

(async() => {
    await client.connect();
    await client.query(
        `CREATE TABLE IF NOT EXISTS document
         (
             id   BIGINT,
             url  VARCHAR(150),
             text TEXT
         );
        CREATE INDEX IF NOT EXISTS idx_gin_document
            ON document
                USING gin (to_tsvector('russian', "text"));
        TRUNCATE document;`
    );

    for (let i = 0; i < links.length - 1; i++) {
        const url = `http://${links[i]}`;
        try {
            let { data } = await axios.get(url);
            await client.query(
                `INSERT INTO document
                 VALUES ($1, $2, $3);`, [i, url, getText(data)]
            );
            console.log(`${i}/${links.length} - ${url}`);
        } catch (e) {
            console.error(i, 'error', url)
        }
    }
    await client.end()
})();


function getText(html) {
    return sanitizeHtml(String(html).replace(/>/g, '> '), {
            allowedTags: []
        })
        .replace(/[\n\t]/g, ' ')
        .replace(/ +/g, ' ')
        .trim()
}