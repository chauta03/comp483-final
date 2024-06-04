import React, { useEffect, useState } from 'react';
import axios from 'axios';

function VoteList() {
    const [votes, setVotes] = useState([]);

    useEffect(() => {
        const fetchVotes = async () => {
            try {
                const response = await axios.get('/get-votes');
                setVotes(response.data);
                console.log(response.data)
            } catch (error) {
                console.error("There was an error!", error);
            }
        };
        fetchVotes();
    }, []);

    return (
        <div>
            <h2>Votes:</h2>
            <ul>
                {votes.map((vote, index) => (
                    <li key={index}>{vote[1]}: {vote[2]}</li>
                ))}
            </ul>
        </div>
    );
}

export default VoteList;
