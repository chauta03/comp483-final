import React, { useState, useEffect } from 'react';
import Vote from './components/Vote';
import VoteList from './components/VoteList';
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
    // <div>
    //   <button onClick={handleClick}>Click me</button>
      
    //   {(typeof data.info === 'undefined') ? (
    //     <p>Loading...</p>
    //   ) : (
    //     data.info.map((i, index) => (
    //       <div key={index}>
    //         <h1>{i}</h1>
    //       </div>
    //     ))
    //   )}

    // </div>

    <div className="App">
          <h1>Voting App</h1>
          <Vote />
          <VoteList />
      </div>
  );
}

export default App;
