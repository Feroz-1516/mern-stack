// src/utils/data.js

/**
 * Array of filter categories for courses
 * @type {Array<{id: string, title: string}>}
 */
export const filterData = [
  {
    id: "1",
    title: "All",
  },
  {
    id: "2",
    title: "Development",
  },
  {
    id: "3",
    title: "Business",
  },
  {
    id: "4",
    title: "Design",
  },
  {
    id: "5",
    title: "Lifestyle",
  },
];

/**
 * API URL for fetching top courses
 * @type {string}
 */
export const apiUrl = "https://codehelp-apis.vercel.app/api/get-top-courses";

/**
 * Fetches courses from the API
 * @returns {Promise<Array<Object>>} Array of course objects
 */
export const getCourses = async () => {
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error('Failed to fetch courses');
    }
    const data = await response.json();
    return Object.values(data.data);
  } catch (error) {
    console.error("Error fetching courses:", error);
    return [];
  }
};

/**
 * Returns an array of unique category names from the filterData
 * @returns {Array<string>} Array of category names
 */
export const getCategories = () => {
  return filterData.map(category => category.title);
};

/**
 * Filters courses based on the selected category
 * @param {Array<Object>} courses - Array of course objects
 * @param {string} category - Selected category
 * @returns {Array<Object>} Filtered array of course objects
 */
export const filterCourses = (courses, category) => {
  if (category === "All") {
    return courses;
  }
  return courses.filter(course => course.category === category);
};

/**
 * Sorts courses based on the given criteria
 * @param {Array<Object>} courses - Array of course objects
 * @param {string} criteria - Sorting criteria (e.g., 'price', 'rating')
 * @returns {Array<Object>} Sorted array of course objects
 */
export const sortCourses = (courses, criteria) => {
  return [...courses].sort((a, b) => {
    if (criteria === 'price') {
      return a.price - b.price;
    } else if (criteria === 'rating') {
      return b.rating - a.rating;
    }
    return 0;
  });
};