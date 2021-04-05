## How to run

1. [Install NodeJs on computer](https://nodejs.org/en/)
1. [Install PosrgreSQL on computer](https://www.postgresql.org/download/)
1. Open project directory `cd <RepoRoot>/task5_searsh-system/search_system`
1. Install dependencies `npm i`
1. Create or use existing database and transfer credentials through [environment variables](#ENV)
1. Run initial script `node init.js`
1. Build app `npm run-script build`
1. Start app `npm start`

### ENV 

```
config = {
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
```
