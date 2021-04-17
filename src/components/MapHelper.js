import React, { useState, useEffect, } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Typography } from '@material-ui/core';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import { DraggableList } from './DraggableList';

function MapHelper() {
    const [enteredText, setEnteredText] = useState("");
    const [result, setResult] = useState([])
    const [sortedItems, setSortedItems] = useState([])
    const [loading, setLoading] = useState(false);

    const attemptSubmit = () => {
        setLoading(true);
        fetch(`/api/map/fromRotation?rotation=${enteredText}`, ).then(res => res.json())
            .then(data => {
                setResult(data)
            }).finally(() => {
                setLoading(false);
            });
    }

    const download = () => {
        fetch(`/api/map/rotationFromData`, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(sortedItems)
        }).then(res => res.json())
        .then(data => {
            var element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(data.join("\n")));
            element.setAttribute('download', "Test.txt");
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        }).finally(() => {
            setLoading(false);
        });

    }

    return (
        <React.Fragment>
            <Typography variant='h4' className="header" gutterBottom>MapRotation Editor</Typography>
            <Grid container spacing={3}>
                {result && result.length > 0 && !loading &&
                    <React.Fragment>
                        <Grid item xs={12}>
                            <Button variant="contained" color="primary" onClick={() => setResult([])}>Return</Button>
                            <Button variant="contained" color="primary" onClick={() => download()}>Save</Button>
                        </Grid>
                        <Grid item xs={12}>
                            <DraggableList items={result} updateSortedItems={(items) => setSortedItems(items)} />
                        </Grid>
                    </React.Fragment>
                }
                {loading &&
                    <Grid item xs={12}>
                        <CircularProgress color='secondary' />
                    </Grid>
                }
                {!loading && result.length === 0 &&
                    <React.Fragment>
                        <Grid item xs={12}>
                            <TextField
                                label="MapRotations"
                                onChange={(e) => setEnteredText(e.target.value)}
                                multiline
                                rows={12}
                                className="rotation-input"
                                variant="outlined"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Button variant="contained" color="primary" onClick={() => attemptSubmit()}>Submit</Button>
                        </Grid>
                    </React.Fragment>
                }

            </Grid>
        </React.Fragment>

    );
}
export default MapHelper;
