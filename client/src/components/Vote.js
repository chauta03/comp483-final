import React, { useState } from 'react';
import axios from 'axios';

function Vote() {
    const [candidate, setCandidate] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/add-vote', { candidate });
            alert(response.data.msg);
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    placeholder="Candidate Name" 
                    value={candidate} 
                    onChange={(e) => setCandidate(e.target.value)} 
                />
                <button type="submit">Vote</button>
            </form>
        </div>
    );
}

export default Vote;
