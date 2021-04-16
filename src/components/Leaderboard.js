import React, { useState, useEffect, } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Typography } from '@material-ui/core';
import Table from 'react-all-in-one-table';

function Leaderboard() {
    const [leaderboardRecords, setLeaderboardRecords] = useState(undefined);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (leaderboardRecords) {
            return
        }
        setLoading(true);
        fetch('/api/leaderboard/get').then(res => res.json())
            .then(data => {
                setLeaderboardRecords(data);
            }).finally(() => {
                setLoading(false);
            });
    }, [leaderboardRecords]);

    let isDesktop = window.matchMedia("(min-width: 1281px)").matches;
    const columns = [
        { dataKey: 'name', label: 'Player', width: isDesktop ? 400 : 300 },
        { dataKey: 'kills', label: isDesktop ? 'Kills' : "K", width: isDesktop ? 300 : 75 },
        { dataKey: 'deaths', label: isDesktop ? 'Deaths' : "D", width: isDesktop ? 300 : 75 },
        { dataKey: 'points', label: isDesktop ? 'Points' : "P", width: isDesktop ? 300 : 75 },
    ]

    return (
        <div style={{ height: '600px'}}>
            <Typography variant='h4' className="header" gutterBottom>Preseason Leaderboard</Typography>
            {loading &&
                <CircularProgress color='secondary' />
            }
            {!loading &&
            <div style={{ minHeight: '40vh', height: '60vh' }}>
                <Table
                    data={leaderboardRecords}
                    columns={columns}
                    defaultOrder="desc"
                    defaultOrderBy="kills"
                    ignoreSearchColumns={["steamId"]}
                    inputClassName={"search-input"}
                />
                </div>
            }
        </div>

    );
}
export default Leaderboard;
