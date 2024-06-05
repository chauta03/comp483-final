import React, { useState, useEffect } from 'react';
import Vote from './components/Vote';
import VoteList from './components/VoteList';
import './App.css';

function App() {

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
      <p className='left-half'>
        <h1>Voting with TF</h1>
        <Vote />
      </p>
      <p className='right-half'>
        <h1>Results</h1>
        <VoteList />
      </p>
      </div>
  );
}

export default App;
