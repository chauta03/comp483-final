import React, { useState, useEffect } from 'react';
import Vote from './components/Vote';
import VoteList from './components/VoteList';
import './App.css';

function App() {

  return (
    <div className="App">
      <p className='App-Question'>
        <p className='question'>What is your favorite programming language?</p>
        <Vote />
      </p>
      <p className='App-Chart'>
        <VoteList />
      </p>
      </div>
  );
}

export default App;
