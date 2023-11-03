import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { Link } from 'react-router-dom';

function NewPage() {

  const [anew,setAnew] = useState(null);
  const { id } = useParams();
  const [rate, setRate] = useState(null);
  
  useEffect(() => {
    // Функция, которую нужно вызывать
    const fetchData = () => {
      fetch(`http://127.0.0.1:8000/api/new/${id}`)
        .then(response => response.json())
        .then(data => setAnew(data));
      const token = localStorage.getItem("FeedBack");
      fetch(`http://127.0.0.1:8000/api/views/add`,{
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
          'FeedBack': token,
        },
          body: JSON.stringify({'new_id':id})
        })
        .then(response => response.json())
        .then(data => {
          if(data.FeedBack) {
            localStorage.setItem("FeedBack", data.FeedBack)
          }})
    };
  
    // Вызываем функцию сразу при загрузке страницы
    fetchData();
  
    // Затем вызываем функцию каждые 19 секунд
    const interval = setInterval(fetchData, 19000);
  
    // Очищаем интервал при размонтировании
    return () => clearInterval(interval);
  }, [rate]);

  
  const handleSubmit = async (num) => {
    const token = localStorage.getItem("FeedBack");
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/feedback/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'FeedBack': token,
        },
        body: JSON.stringify({"new_id":id, "rate":num})
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      setRate(num)


    } catch (error) {
      console.error('There was a problem with the fetch operation: ' + error.message);
    }
  }
  

    if (!anew) {
        return <div>loading...</div>
    }
    
  return (
    <div className="App">
        <div>
        <h1>{anew.title}</h1>
        <h1 onClick={() => handleSubmit(1)}>Лайки: {anew.likes_count}</h1>
        <h1 onClick={() => handleSubmit(0)}>Дизлайки: {anew.dislikes_count}</h1>
        <h1>Просмотры: {anew.views_count}</h1>
        {Object.values(anew.images).map((it) => {
            const image = require(`../images/${it}`)
            return (
                <h1><img style={{height:'150px'}} src={image}></img></h1>
            )
        })}
          {Object.entries(anew.tags).map(([key, tag]) => (
            <Link to={`/tag/${key}`}><span>#{tag}  </span></Link>
          ))}
        <h1>{anew.text}</h1>
        </div>
    </div>
  )
}
export default NewPage;