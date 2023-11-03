import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function MainPage() {
  const [news, setNews] = useState([]);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const handleScroll = () => {
    if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight) return;
    setPage(page => page + 1);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setIsLoading(true);
    fetch(`http://127.0.0.1:8000/api/news?page=${page}`)
      .then(response => response.json())
      .then(data => {
        setNews(oldNews => [...oldNews, ...data.results]);
        setIsLoading(false);
      });
  }, [page]);
  console.log(news)
  return (
    <>
    <div className="App">
      {news.map((aNew) => {
        const image = require(`../images/${aNew.images[0]}`);
          return (
            <>
            <Link to={`/new/${aNew.id}`}>
              <div style={{height:'400px'}}>
                <h1>{aNew.title}</h1>
                <h1>{aNew.text}</h1>
                <h1><img style={{height:'150px'}} src={image}></img></h1>
              </div>
            </Link>
                <div>
                {Object.entries(aNew.tags).map(([key, tag]) => (
                  <Link to={`/tag/${key}`}><span>#{tag}  </span></Link>
                ))}
                </div>
            </>
          )
        })}
      {isLoading && <h2>идет загрузка...</h2>}
    </div>
    </>
  );
}

export default MainPage;