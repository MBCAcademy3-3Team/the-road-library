import React from 'react'
import Header from './Header'; // 추가
import Footer from './Footer' // 아까 만든 Footer.jsx 불러오기

function App() {
  return (
    <div className="App">
      <Header /> {/* 상단에 배치 */}
      
      <main style={{ minHeight: '80vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <h1 className="display-4 fw-bold text-primary">도(道)서관 프로젝트 시작!</h1>
        <p className="lead text-muted">에러 해결 완료. 이제 헤더와 본문을 채우면 됩니다.</p>
      </main>

      <Footer /> {/* 하단에 배치 */}
    </div>
  );
}

export default App;