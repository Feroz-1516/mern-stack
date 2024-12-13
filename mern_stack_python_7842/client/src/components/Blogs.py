import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Blog from './Blog';
import { BASE_URL } from '../config';

const Blogs = () => {
  const [blogs, setBlogs] = useState([]);

  useEffect(() => {
    fetchBlogs();
  }, []);

  const fetchBlogs = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/blogs`);
      setBlogs(response.data);
    } catch (error) {
      console.error('Error fetching blogs:', error);
    }
  };

  return (
    <div>
      <h1>All Blogs</h1>
      {blogs.map((blog) => (
        <Link to={`/blogs/${blog._id}`} key={blog._id}>
          <Blog
            title={blog.title}
            desc={blog.desc}
            img={blog.img}
            user={blog.user.name}
            isUser={false}
            id={blog._id}
          />
        </Link>
      ))}
    </div>
  );
};

export default Blogs;