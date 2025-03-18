import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Blog from './Blog';
import config from '../config';

const Blogs = () => {
  const [blogs, setBlogs] = useState();

  const fetchBlogs = async () => {
    try {
      const response = await axios.get(`${config.BASE_URL}/api/blogs`);
      return response.data;
    } catch (error) {
      console.error('Error fetching blogs:', error);
      return null;
    }
  };

  useEffect(() => {
    fetchBlogs().then((data) => {
      if (data) {
        setBlogs(data.blogs);
      }
    });
  }, []);

  console.log(blogs);

  return (
    <div>
      {blogs &&
        blogs.map((blog) => (
          <Blog
            key={blog._id}
            id={blog._id}
            isUser={localStorage.getItem('userId') === blog.user._id}
            title={blog.title}
            desc={blog.desc}
            img={blog.img}
            user={blog.user.name}
            date={new Date(blog.date).toLocaleDateString()}
          />
        ))}
    </div>
  );
};

export default Blogs;