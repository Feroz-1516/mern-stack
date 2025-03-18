import React from 'react';
import { TextField, Button, Box, Typography, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

const UpdateBlog = () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    // Add logic for form submission
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Update Blog
      </Typography>
      <TextField
        fullWidth
        margin="normal"
        label="Email address"
        type="email"
        variant="outlined"
        required
      />
      <FormControl fullWidth margin="normal">
        <InputLabel id="example-select-label">Example select</InputLabel>
        <Select
          labelId="example-select-label"
          id="example-select"
          label="Example select"
          defaultValue=""
        >
          <MenuItem value={1}>1</MenuItem>
          <MenuItem value={2}>2</MenuItem>
          <MenuItem value={3}>3</MenuItem>
          <MenuItem value={4}>4</MenuItem>
          <MenuItem value={5}>5</MenuItem>
        </Select>
      </FormControl>
      <FormControl fullWidth margin="normal">
        <InputLabel id="example-multiple-select-label">Example multiple select</InputLabel>
        <Select
          labelId="example-multiple-select-label"
          id="example-multiple-select"
          multiple
          label="Example multiple select"
          defaultValue={[]}
        >
          <MenuItem value={1}>1</MenuItem>
          <MenuItem value={2}>2</MenuItem>
          <MenuItem value={3}>3</MenuItem>
          <MenuItem value={4}>4</MenuItem>
          <MenuItem value={5}>5</MenuItem>
        </Select>
      </FormControl>
      <TextField
        fullWidth
        margin="normal"
        label="Example textarea"
        multiline
        rows={3}
        variant="outlined"
      />
      <Button type="submit" variant="contained" color="primary" sx={{ marginTop: 2 }}>
        Submit
      </Button>
    </Box>
  );
};

export default UpdateBlog;