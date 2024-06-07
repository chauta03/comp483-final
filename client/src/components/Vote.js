import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import "./components.css";


Chart.register(...registerables);

function Vote() {
    const [id, setID] = useState('');
    const [votes, setVotes] = useState([]);

    const handleVote = async (candidateName) => {
        try {
            const response = await axios.post('/add-vote', { candidate: candidateName });
            const votes = await axios.get('/get-votes');
            setID(response.data);
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    useEffect(() => {
        const fetchVotes = async () => {
            try {
                const response = await axios.get('/get-votes');
                // Convert the raw data into an array of objects and sort by the number of votes
                const formattedVotes = Object.entries(response.data).map(([candidate, ids]) => ({
                    candidate,
                    ids
                })).sort((a, b) => b.ids.length - a.ids.length);
                setVotes(formattedVotes);
                console.log(formattedVotes);
            } catch (error) {
                console.error("There was an error!", error);
            }
        };
        fetchVotes();
    }, [handleVote]);

    // Prepare data for the chart
    const chartData = {
        labels: votes.map(vote => vote.candidate),
        datasets: [
            {
                label: '# of Votes',
                data: votes.map(vote => vote.ids.length),
                backgroundColor: '#F0EBE3',
                borderColor: 'white',
                borderWidth: 3,
                font: 'white',
                color: 'white',
            }
        ],
    };

    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0 // Ensure no decimals
                }
            }
        }
    };

    return (
        <div className='Big-Vote-Container'>
            <div className='Vote-Container'>
                <p className='Vote-Question'>What is your favorite programming language?</p>
                <p className='Vote-Button-Container'>
                    <button className='Vote-Button' onClick={() => handleVote('Python')}>Python</button>
                    <button className='Vote-Button' onClick={() => handleVote('Java')}>Java</button>
                    <button className='Vote-Button' onClick={() => handleVote('C')}>C</button>
                    <button className='Vote-Button' onClick={() => handleVote('JavaScript')}>JavaScript</button>
                    <button className='Vote-Button' onClick={() => handleVote('R')}>R</button>
                </p>
                
                <p className='Confirm-Line'>Your vote was added with ID: {id}</p>
            </div>
            <div className='VoteList-container'>
                <p className='VoteList-show-ID'>
                <p className='VoteList-title'>Votes List</p>
                <ul className='VoteList-list'>
                    <table className='VoteList-table'>
                        <thead>
                            <tr>
                                <th>Languages</th>
                                <th># Votes</th>
                                <th>IDs</th>
                            </tr>
                        </thead>
                        <tbody>
                            {votes.map((vote, index) => (
                                <tr key={index}>
                                    <td>{vote.candidate}</td>
                                    <td>{vote.ids.length}</td>
                                    <td className='VoteList-id-list'>{vote.ids.join(', ')}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </ul>
            </p>
            
            <p className='VoteList-Vote-Chart'>
                <p className='VoteList-title-Chart'>Votes Chart</p>
                <Bar classNam='VoteList-bar' data={chartData} options={chartOptions} />
            </p>
            
        </div>
        </div>
        
    );
}

export default Vote;
