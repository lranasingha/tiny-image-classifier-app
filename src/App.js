import {Box, Grid, Typography, Button, Avatar} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';
import AddAPhotoIcon from '@material-ui/icons/AddAPhoto';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import {post} from 'axios';
import React, {Component} from 'react';
import './App.css';

class App extends Component {
    constructor() {
        super()
        this.selectedimage = ""
        this.state = {
            file: null,
            classifier_result: null
        }
    }

    classify = (evt) => {
        evt.preventDefault();
        this.state.classifier_result = ""
        const file = this.state.file
        const url = 'http://localhost:5000/api/classify';
        const formData = new FormData();
        formData.append('file', file)
        const config = {
            headers: {
                'content-type': 'multipart/form-data'
            }
        }
        post(url, formData, config).then(this.set_classifier_result)
    }

    set_classifier_result = (response) => {
        let subject = response.data.subject;

        if (subject === "unknown") {
            subject = "Hmm.. I don't know that."
        } else {
            subject = "It's a " + subject
        }

        this.classifier_result_text(subject)
    }

    preview_image = (event) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            document.getElementById("preview-img").src = reader.result
        }
        this.state.file = event.target.files[0]
        reader.readAsDataURL(this.state.file);
    }

    classifier_result_text(inner_text) {
        document.getElementById('classifier-out').innerText = inner_text
    }

    useStyles = makeStyles((theme) => ({
        root: {
            flexGrow: 2,
            '& > *': {
                margin: theme.spacing(1),
            },
        },
        input: {
            display: 'none',
        },
        control: {
            padding: theme.spacing(2),
        },
        paper: {
            padding: theme.spacing(2),
            textAlign: 'center',
            color: theme.palette.text.secondary,
        },
        img_preview: {
            width: 100,
            height: 100,
            border: 'none'
        },
        class_result: {
            fontWeight: "bold"
        },

    }));

    render() {
        let styles = this.useStyles;
        return (
            <Box className={styles.root} alignItems="center">
                <Grid container
                      spacing={4}
                      direction="column"
                      alignItems="center"
                      justify="center"
                      style={{minHeight: '100vh'}}>
                    <Grid item xs={12}>
                        <Typography variant="h4">An Image Classifier</Typography>
                    </Grid>

                    <Grid item xs={8} sm={2}>
                        <Typography variant="subtitle1" gutterBottom>Pick an image </Typography>
                    </Grid>
                    <form onSubmit={this.classify}>
                        <Grid item xs={8} sm={6}>
                            <input
                                accept="image/*"
                                id="contained-button-file"
                                multiple
                                type="file"
                                style={{display: "none"}}
                                onChange={this.preview_image}
                            />
                            <label htmlFor="contained-button-file">
                                <AddAPhotoIcon style={{fontSize: 50}} onClick={() => {
                                    this.classifier_result_text('')
                                }}>
                                </AddAPhotoIcon>
                            </label>
                        </Grid>
                        <Grid item xs={12}><img id="preview-img" alt=" " width="150px" height="150px"
                                                className={styles.img_preview} src=""/></Grid>
                        <Grid item xs={12} sm={8}>
                            <Typography id="classifier-out" variant="subtitle1" className={styles.class_result}
                                        gutterBottom>{this.classifier_result}</Typography>
                        </Grid>
                        <Grid item xs={8} sm={2}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="default"
                                className={styles.button}
                                startIcon={<CloudUploadIcon/>}>
                                Upload
                            </Button>
                        </Grid>
                    </form>
                </Grid>
            </Box>
        );
    }
}

export default App;
