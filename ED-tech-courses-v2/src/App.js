import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Cards from './components/Cards';
import Filter from './components/Filter';
import Spinner from './components/Spinner';
import { getCourses, getCategories, filterCourses } from './utils/data';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('All');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const fetchedCourses = await getCourses();
      setCourses(fetchedCourses);
      const fetchedCategories = getCategories();
      setCategories(['All', ...fetchedCategories]);
    } catch (error) {
      toast.error('Network Error: Unable to fetch courses');
    }
    setLoading(false);
  };

  const handleCategoryChange = (newCategory) => {
    setCategory(newCategory);
  };

  const filteredCourses = filterCourses(courses, category);

  return (
    <div className="min-h-screen flex flex-col bg-bgDark2">
      <Navbar />
      <div className="bg-bgDark2">
        <Filter 
          filterData={categories}
          category={category}
          setCategory={handleCategoryChange}
        />
        <div className="w-11/12 max-w-[1200px] mx-auto flex flex-wrap justify-center items-center min-h-[50vh]">
          {loading ? (
            <Spinner />
          ) : (
            <Cards courses={filteredCourses} category={category} />
          )}
        </div>
      </div>
      <ToastContainer />
    </div>
  );
};

export default App;