import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Blog from './Blog';
import config from '../config';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: '20px auto',
    width: '80%',
  },
  blogContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    marginBottom: '20px',
    boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
  },
}));

const UserBlogs = () => {
  const classes = useStyles();
  const [user, setUser] = useState();
  const id = localStorage.getItem('userId');

  const fetchUserBlogs = async () => {
    try {
      const response = await axios.get(`${config.BASE_URL}/api/blogs/user/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user blogs:', error);
      return null;
    }
  };

  useEffect(() => {
    fetchUserBlogs().then((data) => {
      if (data) {
        setUser(data.user);
      }
    });
  }, []);

  const handleDelete = async (blogId) => {
    try {
      await axios.delete(`${config.BASE_URL}/api/blogs/${blogId}`);
      const updatedData = await fetchUserBlogs();
      if (updatedData) {
        setUser(updatedData.user);
      }
    } catch (error) {
      console.error('Error deleting blog:', error);
    }
  };

  return (
    <div className={classes.container}>
      {user &&
        user.blogs &&
        user.blogs.map((blog) => (
          <div key={blog._id} className={classes.blogContainer}>
            <Blog
              id={blog._id}
              isUser={true}
              title={blog.title}
              description={blog.description}
              imageURL={blog.image}
              userName={user.name}
            />
            <img
              className={classes.blogImage}
              src={blog.image}
              alt={blog.title}
            />
            <button onClick={() => handleDelete(blog._id)}>Delete</button>
          </div>
        ))}
    </div>
  );
};

export default UserBlogs;