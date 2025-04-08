// Filter.test.js

// Mock React
const React = {
  createElement: jest.fn((type, props, ...children) => ({
    type,
    props,
    children
  }))
};

// Mock the Filter component
const Filter = ({ filterData, category, setCategory }) => {
  const filterHandler = (title) => {
    setCategory(title);
  };

  const renderFilterButtons = () => {
    return filterData.map((data) => (
      React.createElement('button', {
        className: filterButtonClassName(category, data.title),
        key: data.id,
        onClick: () => filterHandler(data.title)
      }, data.title)
    ));
  };

  const filterButtonClassName = (category, buttonTitle) => {
    const baseClasses = "text-lg px-2 py-1 rounded-md font-medium text-white bg-black hover:bg-opacity-50 border-2 transition-all duration-300";
    const activeClasses = "bg-opacity-60 border-white";
    const inactiveClasses = "bg-opacity-40 border-transparent";
    
    return `${baseClasses} ${category === buttonTitle ? activeClasses : inactiveClasses}`;
  };

  return React.createElement('div', {
    className: "w-11/12 flex flex-wrap max-w-max space-x-4 gap-y-4 mx-auto py-4 justify-center"
  }, renderFilterButtons());
};

// Test suite
describe('Filter Component', () => {
  // Mock data
  const mockFilterData = [
    { id: 1, title: 'All' },
    { id: 2, title: 'Development' },
    { id: 3, title: 'Business' }
  ];

  // Test cases for filterHandler function
  describe('filterHandler', () => {
    it('should update category when called', () => {
      const setCategory = jest.fn();
      const { filterHandler } = Filter({ filterData: mockFilterData, category: 'All', setCategory });
      
      filterHandler('Development');
      expect(setCategory).toHaveBeenCalledWith('Development');
    });
  });

  // Test cases for renderFilterButtons function
  describe('renderFilterButtons', () => {
    it('should render correct number of buttons', () => {
      const setCategory = jest.fn();
      const result = Filter({ filterData: mockFilterData, category: 'All', setCategory });
      
      expect(result.children.length).toBe(3);
    });

    it('should render buttons with correct properties', () => {
      const setCategory = jest.fn();
      const result = Filter({ filterData: mockFilterData, category: 'All', setCategory });
      
      const buttons = result.children;
      expect(buttons[0].type).toBe('button');
      expect(buttons[0].props.className).toContain('bg-opacity-60 border-white');
      expect(buttons[1].props.className).toContain('bg-opacity-40 border-transparent');
      expect(buttons[2].props.className).toContain('bg-opacity-40 border-transparent');
    });
  });

  // Test cases for filterButtonClassName function
  describe('filterButtonClassName', () => {
    it('should return active class for matching category', () => {
      const { filterButtonClassName } = Filter({ filterData: mockFilterData, category: 'All', setCategory: jest.fn() });
      const result = filterButtonClassName('All', 'All');
      expect(result).toContain('bg-opacity-60 border-white');
    });

    it('should return inactive class for non-matching category', () => {
      const { filterButtonClassName } = Filter({ filterData: mockFilterData, category: 'All', setCategory: jest.fn() });
      const result = filterButtonClassName('All', 'Development');
      expect(result).toContain('bg-opacity-40 border-transparent');
    });
  });

  // Integration test for the entire component
  describe('Filter component integration', () => {
    it('should render correctly with given props', () => {
      const setCategory = jest.fn();
      const result = Filter({ filterData: mockFilterData, category: 'All', setCategory });

      expect(result.type).toBe('div');
      expect(result.props.className).toBe("w-11/12 flex flex-wrap max-w-max space-x-4 gap-y-4 mx-auto py-4 justify-center");
      expect(result.children.length).toBe(3);

      const buttons = result.children;
      expect(buttons[0].props.children).toBe('All');
      expect(buttons[1].props.children).toBe('Development');
      expect(buttons[2].props.children).toBe('Business');
    });
  });
});