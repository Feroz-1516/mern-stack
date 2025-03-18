import React, { useState } from 'react';
import { Box, Button, InputLabel, TextField, Typography } from '@mui/material';
import TextareaAutosize from '@mui/material/TextareaAutosize';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useStyles } from '../utils/utils';
import config from '../config';

const labelStyles = { mb: 1, mt: 2, fontSize: '24px', fontWeight: 'bold' };

const AddBlogs = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [inputs, setInputs] = useState({
    title: '',
    description: '',
    imageURL: '',
  });

  const handleChange = (e) => {
    setInputs((prevState) => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };

  const sendRequest = async () => {
    try {
      const res = await axios.post(`${config.BASE_URL}/api/blogs/add`, {
        title: inputs.title,
        desc: inputs.description,
        img: inputs.imageURL,
        user: localStorage.getItem('userId'),
      });
      return res.data;
    } catch (err) {
      console.error('Error adding blog:', err);
      throw err;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(inputs);
    try {
      const data = await sendRequest();
      console.log(data);
      navigate('/blogs');
    } catch (error) {
      console.error('Error submitting blog:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <Box
          borderRadius={10}
          boxShadow="10px 10px 20px #ccc"
          padding={3}
          margin="auto"
          marginTop={3}
          display="flex"
          flexDirection="column"
          width="80%"
        >
          <Typography
            className={classes.font}
            padding={3}
            color="grey"
            variant="h2"
            textAlign="center"
          >
            Post Your Blog
          </Typography>
          <InputLabel className={classes.font} sx={labelStyles}>
            Title
          </InputLabel>
          <TextField
            className={classes.font}
            name="title"
            onChange={handleChange}
            value={inputs.title}
            margin="normal"
            variant="outlined"
          />
          <InputLabel className={classes.font} sx={labelStyles}>
            Description
          </InputLabel>
          <TextareaAutosize
            className={classes.font}
            name="description"
            onChange={handleChange}
            minRows={10}
            style={{ width: '100%', padding: '10px' }}
            value={inputs.description}
          />
          <InputLabel className={classes.font} sx={labelStyles}>
            ImageURL
          </InputLabel>
          <TextField
            className={classes.font}
            name="imageURL"
            onChange={handleChange}
            value={inputs.imageURL}
            margin="normal"
            variant="outlined"
          />
          <Button
            sx={{ mt: 2, borderRadius: 4 }}
            variant="contained"
            type="submit"
          >
            Submit
          </Button>
        </Box>
      </form>
    </div>
  );
};

export default AddBlogs;