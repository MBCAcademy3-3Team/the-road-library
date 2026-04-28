import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// 1. 부트스트랩 디자인(CSS) 연결
import 'bootstrap/dist/css/bootstrap.min.css';
// 2. 부트스트랩 아이콘 연결
import 'bootstrap-icons/font/bootstrap-icons.css';
// 3. 부트스트랩 기능(JS) 연결 -> 이게 있어야 메뉴가 가로로 정렬되고 드롭다운이 작동합니다!
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)