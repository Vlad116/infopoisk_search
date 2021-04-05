import Head from 'next/head'
import styles from '../styles/Home.module.css'
import {useCallback, useEffect, useMemo, useState} from "react";
import {useRouter} from "next/router";
import useDebounce from "../hooks/useDebounce.ts";
import axios from "axios";
import debounce from 'lodash.debounce'


export default function Home() {
    const router = useRouter();
    const [results, setResults] = useState([]);
    const query = useMemo(() => router.query.s || '', [router.query.s])

    const onChange = useCallback((e) => {
        router.replace({href: '/', query: {s: e.currentTarget.value}})
    }, [router])

    const getResults = useCallback(debounce(async (q) => {
        const {data} = await axios.get(`/api/search?s=${q}`);
        setResults(data.rows);
    }, 300), [])

    useEffect(() => {
        getResults(query);
    }, [query, getResults])


    return (
        <div className="container">
            <div className="row">
                <div className="col-12">
                    <div className="input-group mb-3 mt-lg-4">
                        <input value={query} onChange={onChange} onKeyPress={e => e.key === 'Enter' && getResults(query)} type="text" className="form-control"
                               placeholder="Введите поисковый запрос"
                               aria-label="Recipient's username" aria-describedby="button-addon2"/>
                        <div className="input-group-append">
                            <button
                                className="btn btn-outline-primary"
                                type="button"
                                id="button-addon2"
                                onClick={() => getResults(query)}
                            >
                                Поиск
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                {results.length ? results.map(result => <div className="col-12 query-answer">
                    <h3><a href={result.url}>{result.url}</a> </h3>
                    <p style={{maxHeight: '45px', overflow: 'hidden'}}>{result.text}</p>
                </div>) :  <div className="col-12 query-answer"><h1>Ничего не найдено :(</h1></div>}
            </div>
        </div>
    )
}