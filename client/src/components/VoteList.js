import React, { useEffect, useState } from 'react';
import axios from 'axios';

function VoteList() {
    const [votes, setVotes] = useState([]);

    useEffect(() => {
        const fetchVotes = async () => {
            try {
                const response = await axios.get('/get-votes');
                // Convert the raw data into an array of objects
                const formattedVotes = Object.entries(response.data).map(([candidate, ids]) => ({
                    candidate,
                    ids
                }));
                setVotes(formattedVotes);
                console.log(formattedVotes);
            } catch (error) {
                console.error("There was an error!", error);
            }
        };
        fetchVotes();
    }, []);

    return (
        <div>
            <ul>
                {votes.map((vote) => (
                    <li key={vote.candidate}>
                        <strong>{vote.candidate}:</strong> {vote.ids.join(', ')}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default VoteList;
