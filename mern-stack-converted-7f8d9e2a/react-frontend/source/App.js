import './App.css';
import { Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import React from 'react';
import Login from './components/Login';
import Blogs from './components/Blogs';
import UserBlogs from './components/UserBlogs';
import AddBlogs from './components/AddBlogs';
import BlogDetail from './components/BlogDetail';

function App() {
  return (
    <React.Fragment>
      <header>
        <Header />
      </header>
      <main>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/blogs" element={<Blogs />} />
          <Route path="/myBlogs" element={<UserBlogs />} />
          <Route path="/myBlogs/:id" element={<BlogDetail />} />
          <Route path="/blogs/add" element={<AddBlogs />} />
        </Routes>
      </main>
    </React.Fragment>
  );
}

export default App;