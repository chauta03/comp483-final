import React, { useState } from 'react';
import axios from 'axios';
import "./components.css";

function Vote() {
    const [id, setID] = useState('');

    const handleVote = async (candidateName) => {
        try {
            const response = await axios.post('/add-vote', { candidate: candidateName });
            setID(response.data);
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    return (
        <div className='Vote-Container'>
            <p className='Vote-Button-Container'>
                <button className='Vote-Button' onClick={() => handleVote('Python')}>Python</button>
                <button className='Vote-Button' onClick={() => handleVote('Java')}>Java</button>
                <button className='Vote-Button' onClick={() => handleVote('C')}>C</button>
                <button className='Vote-Button' onClick={() => handleVote('JavaScript')}>JavaScript</button>
                <button className='Vote-Button' onClick={() => handleVote('R')}>R</button>
            </p>
            
            <p className='Confirm-Line'>Your vote was added with ID: {id}</p>
        </div>
    );
}

export default Vote;
