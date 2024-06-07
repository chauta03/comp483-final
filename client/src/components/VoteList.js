import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import './components.css';

Chart.register(...registerables);

function VoteList() {
    const [votes, setVotes] = useState([]);

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
    }, []);

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

    // I want to style this
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
    );
}

export default VoteList;
