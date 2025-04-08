// Card.test.js

// Mock external dependencies
jest.mock('react-icons/fc', () => ({
  FcLike: () => 'FcLike',
  FcLikePlaceholder: () => 'FcLikePlaceholder',
}));

jest.mock('react-toastify', () => ({
  toast: {
    success: jest.fn(),
    warning: jest.fn(),
  },
}));

// Mock React and useState
const React = require('react');
const useState = jest.fn();
React.useState = useState;

// Helper function to create a shallow renderer
const createShallowRenderer = require('react-test-renderer/shallow');

// Component to be tested
const Card = ({ course, likedCourses, setLikedCourses }) => {
  const clickHandler = () => {
    if (likedCourses.includes(course.id)) {
      setLikedCourses(prev => prev.filter(cid => cid !== course.id));
      toast.warning("Like removed");
    } else {
      setLikedCourses(prev => [...prev, course.id]);
      toast.success("Liked Successfully");
    }
  };

  return (
    <div className='w-[300px] bg-bgDark bg-opacity-80 rounded-md overflow-hidden'>
      <div className='relative'>
        <img src={course.image.url} alt={course.title} />
        <div className='w-[40px] h-[40px] bg-white rounded-full absolute right-2 bottom-[-12px] grid place-items-center'>
          <button onClick={clickHandler} aria-label={likedCourses.includes(course.id) ? "Unlike course" : "Like course"}>
            {likedCourses.includes(course.id) 
              ? <FcLike fontSize="1.75rem" />
              : <FcLikePlaceholder fontSize="1.75rem" />
            }
          </button>
        </div>
      </div>
      <div className='p-4'>
        <p className="text-white font-semibold text-lg leading-6">{course.title}</p>
        <p className='mt-2 text-white'>
          {course.description.length > 100 
            ? `${course.description.substr(0, 100)}...`
            : course.description
          }
        </p>
      </div>
    </div>
  );
};

// Test suite
describe('Card Component', () => {
  let renderer;
  let setLikedCoursesMock;

  beforeEach(() => {
    renderer = createShallowRenderer();
    setLikedCoursesMock = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockCourse = {
    id: '1',
    image: { url: 'https://example.com/image.jpg' },
    title: 'React Course',
    description: 'Learn React from scratch',
  };

  test('clickHandler adds course to likedCourses when not liked', () => {
    const props = {
      course: mockCourse,
      likedCourses: [],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const button = instance.props.children[0].props.children[1].props.children;
    
    button.props.onClick();

    expect(setLikedCoursesMock).toHaveBeenCalledWith(expect.any(Function));
    const setStateCb = setLikedCoursesMock.mock.calls[0][0];
    expect(setStateCb([])).toEqual(['1']);
  });

  test('clickHandler removes course from likedCourses when already liked', () => {
    const props = {
      course: mockCourse,
      likedCourses: ['1'],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const button = instance.props.children[0].props.children[1].props.children;
    
    button.props.onClick();

    expect(setLikedCoursesMock).toHaveBeenCalledWith(expect.any(Function));
    const setStateCb = setLikedCoursesMock.mock.calls[0][0];
    expect(setStateCb(['1'])).toEqual([]);
  });

  test('renderLikeButton shows FcLike when course is liked', () => {
    const props = {
      course: mockCourse,
      likedCourses: ['1'],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const likeButton = instance.props.children[0].props.children[1].props.children.props.children;

    expect(likeButton.type).toBe('FcLike');
  });

  test('renderLikeButton shows FcLikePlaceholder when course is not liked', () => {
    const props = {
      course: mockCourse,
      likedCourses: [],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const likeButton = instance.props.children[0].props.children[1].props.children.props.children;

    expect(likeButton.type).toBe('FcLikePlaceholder');
  });

  test('renderDescription truncates long description', () => {
    const longDescription = 'This is a very long description that exceeds 100 characters and should be truncated in the output with an ellipsis at the end.';
    const props = {
      course: { ...mockCourse, description: longDescription },
      likedCourses: [],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const description = instance.props.children[1].props.children[1].props.children;

    expect(description).toBe('This is a very long description that exceeds 100 characters and should be truncated in the output with an ...');
  });

  test('renderDescription does not truncate short description', () => {
    const shortDescription = 'Short description';
    const props = {
      course: { ...mockCourse, description: shortDescription },
      likedCourses: [],
      setLikedCourses: setLikedCoursesMock,
    };

    renderer.render(<Card {...props} />);
    const instance = renderer.getRenderOutput();
    const description = instance.props.children[1].props.children[1].props.children;

    expect(description).toBe('Short description');
  });
});