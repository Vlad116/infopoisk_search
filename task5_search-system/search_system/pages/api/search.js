// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import { Client } from 'pg';

const client = new Client({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'postgres',
    database: 'infosearch'
});
client.connect();

export default async(req, res) => {
    const results = await client.query(
        `SELECT id,
                url,
                text,
                ts_rank(to_tsvector("text"),
                        plainto_tsquery($1))
         FROM document
         WHERE to_tsvector("text") @@ plainto_tsquery($1)
         ORDER BY ts_rank(to_tsvector("text"), plainto_tsquery($1)) DESC;`, [req.query.s]);

    res.status(200).json(results)
}