import React, { useState, useEffect } from 'react';

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch('/vote')
      .then(res => res.json())
      .then(data => setData(data))
                    console.log(data)
  } , []) 

  const handleClick = (e) => {
    e.preventDefault();
    console.log('The link was clicked.');
  }

  return (
    <div>
      <button onClick={handleClick}>Click me</button>
      
      {(typeof data.info === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        data.info.map((i, index) => (
          <div key={index}>
            <h1>{i}</h1>
          </div>
        ))
      )}

    </div>
  );
}

export default App;
