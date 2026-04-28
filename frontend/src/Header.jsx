import React from 'react';

const Header = () => {
  // 임시 세션 데이터 (나중에 Flask API와 연결하면 실제 데이터로 대체됩니다)
  const session = {
    user_id: null, // 로그인 테스트를 하려면 'user123'으로 바꿔보세요
    user_role: 'user', // 'admin', 'manager', 'user'
    user_nickname: '도전자',
  };

  return (
    <nav className="navbar navbar-expand-lg sticky-top py-3 bg-white shadow-sm">
      <style>
        {`
          .dropdown-toggle::after {
            border: none !important;
            margin: 0 !important;
            display: inline-block;
          }
          :root {
            --primary-teal: #20c997; /* 기존 CSS 변수 유지 */
          }
        `}
      </style>

      <div className="container">
        {/* 로고 영역 */}
        <a className="navbar-brand d-flex align-items-center" href="/">
          {/* 이미지는 나중에 frontend/public/logo 폴더를 만들어서 넣으면 됩니다 */}
          <img 
            src="/logo/the_road_library_logo.png" 
            alt="로고" 
            width="60" 
            height="60" 
            className="me-2" 
          />
          <span className="fw-bold">도(道)서관</span>
        </a>

        {/* 모바일 토글 버튼 */}
        <button 
          className="navbar-toggler border-0 shadow-none" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <div className="flex-grow-1"></div>

          {/* 메뉴 리스트 */}
          <ul className="navbar-nav gap-lg-4 mt-3 mt-lg-0">
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" id="introDropdown" data-bs-toggle="dropdown">소개</a>
              <ul className="dropdown-menu border-0 shadow-sm">
                <li><a className="dropdown-item" href="/introduce/background">프로젝트 배경</a></li>
                <li><a className="dropdown-item" href="/introduce/logo">BI 소개</a></li>
                <li><a className="dropdown-item" href="/introduce/process">개발 과정</a></li>
                <li><a className="dropdown-item" href="/introduce/features">홈페이지 소개</a></li>
              </ul>
            </li>
            <li className="nav-item"><a className="nav-link" href="/model">도(道)와주세요</a></li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" id="boardDropdown" data-bs-toggle="dropdown">도(道)란도란</a>
              <ul className="dropdown-menu border-0 shadow-sm">
                <li><a className="dropdown-item" href="/board/list?category=free">자유 게시판</a></li>
                <li><a className="dropdown-item" href="/board/list?category=info">정보 게시판</a></li>
                <li><a className="dropdown-item" href="/board/list?category=qna">도(道)를 아십니까?</a></li>
              </ul>
            </li>
            <li className="nav-item"><a className="nav-link" href="/tip">도(道)움말</a></li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" id="mypageDropdown" data-bs-toggle="dropdown">마이페이지</a>
              <ul className="dropdown-menu border-0 shadow-sm">
                <li><a className="dropdown-item" href="/mypage">회원 정보</a></li>
                <li><a className="dropdown-item" href="/mypage/my_activity">나의 활동</a></li>
                <li><a className="dropdown-item" href="/mypage/ai_results">AI 분석 결과</a></li>
              </ul>
            </li>
            {['admin', 'manager'].includes(session.user_role) && (
              <li className="nav-item"><a className="nav-link" href="/admin">관리자</a></li>
            )}
          </ul>

          {/* 우측 로그인/사용자 정보 */}
          <div className="d-flex align-items-center gap-3 flex-grow-1 justify-content-lg-end mt-4 mt-lg-0 pb-3 pb-lg-0">
            {!session.user_id ? (
              <>
                <a href="/auth/login" className="text-decoration-none text-muted small fw-medium">로그인</a>
                <a href="/auth/signup" className="btn btn-sm text-white px-3 rounded-pill shadow-sm" style={{ backgroundColor: 'var(--primary-teal)', fontSize: '0.85rem' }}>
                  회원가입
                </a>
              </>
            ) : (
              <div className="d-flex align-items-center bg-light px-3 py-1 rounded-pill border shadow-sm w-auto">
                {session.user_role === 'admin' ? (
                  <span className="badge rounded-pill bg-danger me-2" style={{ fontSize: '0.7rem' }}>도(관리자)</span>
                ) : session.user_role === 'manager' ? (
                  <span className="badge rounded-pill text-dark me-2" style={{ backgroundColor: '#fd8a69', fontSize: '0.7rem' }}>레(매니저)</span>
                ) : (
                  <span className="badge rounded-pill me-2" style={{ backgroundColor: 'var(--primary-teal)', fontSize: '0.7rem' }}>미(일반)</span>
                )}
                <span className="small text-dark fw-bold">
                  {session.user_nickname} <span className="fw-normal text-muted">님</span>
                </span>
                <div className="vr mx-3" style={{ height: '15px', marginTop: '3px' }}></div>
                <a href="/auth/logout" className="text-decoration-none text-danger small fw-medium d-flex align-items-center" title="로그아웃">
                  <i className="bi bi-box-arrow-right me-1"></i> <span>로그아웃</span>
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Header;