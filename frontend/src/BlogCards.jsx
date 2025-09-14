import React from 'react';

const blogs = [
  {
    title: 'Summer Sale Success: Top Ad Copy Tips',
    excerpt: 'Discover proven strategies and examples for crafting irresistible summer sale campaigns that convert.',
    author: 'Jane Doe',
    date: 'July 2025',
    image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Boost Engagement with Seasonal Offers',
    excerpt: 'Learn how to leverage seasonal trends and create offers that drive engagement and sales.',
    author: 'John Smith',
    date: 'June 2025',
    image: 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
  },
  {
    title: 'Email Marketing: Best Practices for 2025',
    excerpt: 'Stay ahead with the latest email marketing techniques and examples for high open rates.',
    author: 'Emily Clark',
    date: 'May 2025',
    image: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80',
  },
];

export default function BlogCards() {
  return (
    <div className="blog-section">
      <h2>Featured Marketing Blogs</h2>
      <div className="blog-cards">
        {blogs.map((blog, idx) => (
          <div className="blog-card" key={idx}>
            <img src={blog.image} alt={blog.title} className="blog-image" />
            <div className="blog-content">
              <h3>{blog.title}</h3>
              <p>{blog.excerpt}</p>
              <div className="blog-meta">
                <span>{blog.author}</span> | <span>{blog.date}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
