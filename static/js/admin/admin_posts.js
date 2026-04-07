async function openBoardDetail(id) {
    try {
        const res  = await fetch(`/admin/board/detail/${id}`);
        const data = await res.json();

        // [체크 1] 데이터가 어디 들어있는지 콘솔로 확인 (이거 꼭 보세요!)
        console.log("받은 데이터 전체:", data);

        // [체크 2] 데이터가 감싸져 있을 경우를 대비 (데이터가 data.board 안에 있을 수도 있음)
        const b = (data.id) ? data : data.board;

        if (!b) {
            alert("데이터 구조가 이상합니다. 콘솔을 확인하세요.");
            return;
        }

        // [체크 3] HTML 엘리먼트가 있는지 확인하며 바인딩
        // 텍스트 정보들
        const elTitle   = document.getElementById('detail_title');
        const elAuthor  = document.getElementById('detail_author');
        const elDate    = document.getElementById('detail_created_at');
        const elVisits  = document.getElementById('detail_visits');
        const elContent = document.getElementById('detail_content');

        if (elTitle)   elTitle.textContent   = b.title   || '제목 없음';
        if (elAuthor)  elAuthor.textContent  = b.author  || b.nickname || '작성자 정보 없음';
        if (elDate)    elDate.textContent    = b.created_at || '-';
        if (elVisits)  elVisits.textContent  = b.visits  || 0;

        // 본문 내용 (가장 중요!)
        if (elContent) {
            elContent.innerHTML = b.content || '<span style="color:gray">내용이 없습니다.</span>';
        }

        // --- 게시글 신고 렌더링 ---
        const reportWrap = document.getElementById('detail_reports_wrap');
        const reportArea = document.getElementById('detail_reports');
        if (b.reports && b.reports.length > 0) {
            reportArea.innerHTML = b.reports.map((r, i) =>
                `<div><strong>${i+1}. ${r.reason}</strong>: ${r.detail || ''}</div>`
            ).join('');
            reportWrap.style.display = 'block';
        } else {
            reportWrap.style.display = 'none';
        }

        // --- 댓글 신고 렌더링 ---
        const commentWrap = document.getElementById('detail_comments_wrap');
        const commentArea = document.getElementById('detail_comments');
        if (b.comment_reports && b.comment_reports.length > 0) {
            commentArea.innerHTML = b.comment_reports.map((c, i) => `
                <div style="margin-bottom:10px; border-bottom:1px dashed #ccc;">
                    <div style="color:orange;">[${c.reason}]</div>
                    <div>${c.content || '내용없음'}</div>
                </div>
            `).join('');
            commentWrap.style.display = 'block';
        } else {
            commentWrap.style.display = 'none';
        }

        // 모달 열기
        document.getElementById('boardDetailModal').classList.add('open');

    } catch (err) {
        console.error("JS 실행 중 에러 발생:", err);
        alert("데이터를 화면에 뿌리는 중 에러가 발생했습니다.");
    }
}
function closeBoardDetail() {
    const modal = document.getElementById('boardDetailModal');
    modal.classList.remove('open');

    // 다음 글 열 때 이전 내용이 잠깐 보이는 "잔상" 방지
    document.getElementById('detail_content').innerHTML = '';
    document.getElementById('detail_reports').innerHTML = '';
}
