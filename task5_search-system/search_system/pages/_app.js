import '../styles/globals.scss'

function MyApp({Component, pageProps}) {
    return <>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container">
                <a className="navbar-brand" href="#">MyGoogle</a>
            </div>
        </nav>
        <Component {...pageProps} />
    </>
}

export default MyApp
