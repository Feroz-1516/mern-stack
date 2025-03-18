import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Box, Button, InputLabel, TextField, Typography } from '@mui/material';
import config from '../config';

const labelStyles = { mb: 1, mt: 2, fontSize: '24px', fontWeight: 'bold' };

const BlogDetail = () => {
  const navigate = useNavigate();
  const [blog, setBlog] = useState();
  const { id } = useParams();
  const [inputs, setInputs] = useState({});

  const handleChange = (e) => {
    setInputs((prevState) => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };

  const fetchDetails = async () => {
    try {
      const res = await axios.get(`${config.BASE_URL}/api/blogs/${id}`);
      return res.data;
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDetails().then((data) => {
      setBlog(data.blog);
      setInputs({
        title: data.blog.title,
        description: data.blog.description,
      });
    });
  }, [id]);

  const sendRequest = async () => {
    try {
      const res = await axios.put(`${config.BASE_URL}/api/blogs/update/${id}`, {
        title: inputs.title,
        description: inputs.description,
      });
      return res.data;
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendRequest()
      .then((data) => console.log(data))
      .then(() => navigate('/myBlogs/'));
  };

  return (
    <div>
      {inputs && (
        <form onSubmit={handleSubmit}>
          <Box
            sx={{
              border: 3,
              borderColor: 'linear-gradient(90deg, rgba(58,75,180,1) 2%, rgba(116,49,110,1) 36%, rgba(2,0,161,1) 73%, rgba(69,92,252,1) 100%)',
              borderRadius: 10,
              boxShadow: '10px 10px 20px #ccc',
              padding: 3,
              margin: 'auto',
              marginTop: 3,
              display: 'flex',
              flexDirection: 'column',
              width: '80%',
            }}
          >
            <Typography
              sx={{
                fontWeight: 'bold',
                padding: 3,
                color: 'grey',
                variant: 'h2',
                textAlign: 'center',
              }}
            >
              Post Your Blog
            </Typography>
            <InputLabel sx={labelStyles}>Title</InputLabel>
            <TextField
              name="title"
              onChange={handleChange}
              value={inputs.title}
              margin="normal"
              variant="outlined"
            />
            <InputLabel sx={labelStyles}>Description</InputLabel>
            <TextField
              name="description"
              onChange={handleChange}
              value={inputs.description}
              margin="normal"
              variant="outlined"
            />
            <Button
              sx={{ mt: 2, borderRadius: 4 }}
              variant="contained"
              color="warning"
              type="submit"
            >
              Submit
            </Button>
          </Box>
        </form>
      )}
    </div>
  );
};

export default BlogDetail;