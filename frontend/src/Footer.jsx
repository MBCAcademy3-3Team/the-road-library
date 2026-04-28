import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-dark text-white pt-4 pb-2 mt-5">
      <div className="container text-center">
        <p>© 2026 도(道)서관 프로젝트. All rights reserved.</p>
        <div className="mb-3">
          <a href="#" className="text-white me-3 text-decoration-none">이용약관</a>
          <a href="#" className="text-white text-decoration-none">개인정보처리방침</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;