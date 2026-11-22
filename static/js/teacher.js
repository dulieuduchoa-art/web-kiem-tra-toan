/**
 * Teacher Management Dashboard Logic
 * - Exam creator with Kho_SGK_SBT lesson selector, raw text parser, and visual editor
 * - Standard 22-question matrix validator
 * - Preview modal with KaTeX
 * - Student results table filtered by class
 * - Professional Excel (.xlsx) exporter
 */

const TeacherPortal = {
  currentQuestions: [],
  curriculumData: null,
  activeExamId: null,
  currentResultsExamId: null,
  currentClassFilter: 'Tất cả',

  init: function() {
    this.checkAuth();
    this.loadCurriculum();
    this.loadExamsList();
    this.bindEvents();
  },

  // --- Teacher Authentication ---
  checkAuth: function() {
    const token = sessionStorage.getItem('teacher_token');
    if (!token) {
      document.getElementById('auth-modal').classList.remove('hidden');
    } else {
      document.getElementById('auth-modal').classList.add('hidden');
      document.getElementById('teacher-app-content').classList.remove('hidden');
    }
  },

  login: async function() {
    const password = document.getElementById('teacher-pw-input').value;
    if (!password) {
      App.showToast('Vui lòng nhập mật khẩu!', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/auth/teacher', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Sai mật khẩu!');
      }

      sessionStorage.setItem('teacher_token', data.token);
      document.getElementById('auth-modal').classList.add('hidden');
      document.getElementById('teacher-app-content').classList.remove('hidden');
      App.showToast('Đăng nhập thành công!', 'success');
      this.loadExamsList();
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  },

  logout: function() {
    sessionStorage.removeItem('teacher_token');
    window.location.reload();
  },

  // --- Curriculum & Kho_SGK_SBT ---
  loadCurriculum: async function() {
    try {
      const res = await fetch('/api/curriculum');
      const data = await res.json();
      this.curriculumData = data.curriculum;
      this.populateCurriculumSelectors();
      this.loadKhoSgkFiles();
    } catch (e) {
      console.error('Error loading curriculum:', e);
    }
  },

  populateCurriculumSelectors: function() {
    const gradeSelect = document.getElementById('curriculum-grade');
    const bookSelect = document.getElementById('curriculum-book');
    const chapterSelect = document.getElementById('curriculum-chapter');

    if (!gradeSelect || !bookSelect || !chapterSelect) return;

    const onGradeChange = () => {
      const g = gradeSelect.value;
      const books = this.curriculumData[g] || {};
      bookSelect.innerHTML = '';
      for (const bKey in books) {
        const opt = document.createElement('option');
        opt.value = bKey;
        opt.textContent = books[bKey].name;
        bookSelect.appendChild(opt);
      }
      onBookChange();
    };

    const onBookChange = () => {
      const g = gradeSelect.value;
      const b = bookSelect.value;
      const chapters = (this.curriculumData[g] && this.curriculumData[g][b] && this.curriculumData[g][b].chapters) || [];
      chapterSelect.innerHTML = '';
      chapters.forEach(ch => {
        const optGroup = document.createElement('optgroup');
        optGroup.label = ch.title;
        (ch.lessons || []).forEach(ls => {
          const lOpt = document.createElement('option');
          lOpt.value = ls.id;
          lOpt.textContent = ls.title;
          optGroup.appendChild(lOpt);
        });
        chapterSelect.appendChild(optGroup);
      });
    };

    gradeSelect.addEventListener('change', onGradeChange);
    bookSelect.addEventListener('change', onBookChange);

    // Initial trigger
    onGradeChange();
  },

  loadFromCurriculum: async function() {
    const grade = document.getElementById('curriculum-grade').value;
    const book = document.getElementById('curriculum-book').value;
    const lessonId = document.getElementById('curriculum-chapter').value;
    const lessonTitle = document.getElementById('curriculum-chapter').selectedOptions[0]?.textContent || '';
    const bookName = document.getElementById('curriculum-book').selectedOptions[0]?.textContent || '';

    const defaultTitle = `Kiểm tra Toán ${grade} - ${lessonTitle} (${bookName})`;
    document.getElementById('exam-title-input').value = defaultTitle;
    document.getElementById('exam-grade-input').value = grade;

    try {
      const res = await fetch('/api/curriculum/generate-exam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          grade,
          book,
          lesson_id: lessonId,
          title: defaultTitle,
          duration_minutes: parseInt(document.getElementById('exam-duration-input').value) || 50
        })
      });

      const data = await res.json();
      this.currentQuestions = data.exam.questions || [];
      this.renderQuestionsList();
      this.updateMatrixWidget();
      App.showToast(`Đã nạp ${this.currentQuestions.length} câu chuẩn ma trận Bộ GD&ĐT!`, 'success');
    } catch (err) {
      App.showToast('Lỗi khi nạp từ kho bài học: ' + err.message, 'error');
    }
  },

  loadKhoSgkFiles: async function() {
    try {
      const res = await fetch('/api/kho-sgk-sbt/files');
      const data = await res.json();
      const container = document.getElementById('kho-files-list');
      if (!container) return;

      container.innerHTML = '';
      const filesTree = data.files || {};

      let hasFiles = false;

      for (const grade in filesTree) {
        const gradeSec = document.createElement('div');
        gradeSec.className = 'mb-6';
        gradeSec.innerHTML = `<h3 class="text-base font-bold text-slate-800 mb-3 flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-blue-600"></span>
          Khối ${grade.replace('Khoi_', '')}
        </h3>`;

        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-3';

        for (const book in filesTree[grade]) {
          const files = filesTree[grade][book] || [];
          files.forEach(f => {
            hasFiles = true;
            const bookReadable = book.replace(/_/g, ' ');
            const card = document.createElement('div');
            card.className = 'p-3 bg-white rounded-xl border border-slate-200 shadow-sm flex items-center justify-between gap-3 hover:border-blue-400 transition-all';
            card.innerHTML = `
              <div class="flex items-center gap-3 overflow-hidden">
                <div class="w-10 h-10 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center font-bold text-xs flex-shrink-0">
                  PDF
                </div>
                <div class="truncate">
                  <div class="font-medium text-sm text-slate-800 truncate" title="${f.filename}">${f.filename}</div>
                  <div class="text-xs text-slate-500">${bookReadable} • ${f.size_mb} MB</div>
                </div>
              </div>
              <a href="${f.url}" target="_blank" class="flex-shrink-0 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-blue-50 hover:text-blue-600 text-xs font-semibold text-slate-700 transition-colors">
                Mở file ↗
              </a>
            `;
            grid.appendChild(card);
          });
        }
        gradeSec.appendChild(grid);
        container.appendChild(gradeSec);
      }

      if (!hasFiles) {
        container.innerHTML = '<div class="text-slate-500 text-sm">Chưa có file PDF nào trong thư mục Kho_SGK_SBT.</div>';
      }
    } catch (e) {
      console.error(e);
    }
  },

  // --- Text Parser Import ---
  loadSampleTemplate: async function() {
    try {
      const res = await fetch('/api/exams/sample-template');
      const data = await res.json();
      document.getElementById('import-textarea').value = data.template;
      App.showToast('Đã nạp đề mẫu vào khung soạn thảo!', 'info');
    } catch (e) {}
  },

  parseImportText: async function() {
    const raw = document.getElementById('import-textarea').value;
    if (!raw.trim()) {
      App.showToast('Vui lòng dán nội dung đề thi!', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/exams/parse-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text: raw })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Phân tích thất bại!');

      if (data.questions.length === 0) {
        App.showToast('Không tìm thấy câu hỏi nào hợp lệ từ văn bản!', 'error');
        return;
      }

      this.currentQuestions = data.questions;
      this.renderQuestionsList();
      this.updateMatrixWidget();
      App.showToast(`Phân tích thành công ${data.questions.length} câu hỏi!`, 'success');
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  },

  // --- Matrix & Questions Editing ---
  updateMatrixWidget: function() {
    const p1Count = this.currentQuestions.filter(q => q.part === 1).length;
    const p2Count = this.currentQuestions.filter(q => q.part === 2).length;
    const p3Count = this.currentQuestions.filter(q => q.part === 3).length;
    const totalCount = this.currentQuestions.length;

    const p1Score = p1Count * 0.25;
    const p2Score = p2Count * 1.0;
    const p3Score = p3Count * 0.5;
    const totalScore = (p1Score + p2Score + p3Score).toFixed(2);

    document.getElementById('matrix-p1-count').textContent = `${p1Count}/12 câu`;
    document.getElementById('matrix-p1-score').textContent = `${p1Score.toFixed(2)}đ`;
    document.getElementById('matrix-p2-count').textContent = `${p2Count}/4 câu`;
    document.getElementById('matrix-p2-score').textContent = `${p2Score.toFixed(2)}đ`;
    document.getElementById('matrix-p3-count').textContent = `${p3Count}/6 câu`;
    document.getElementById('matrix-p3-score').textContent = `${p3Score.toFixed(2)}đ`;
    document.getElementById('matrix-total-count').textContent = `${totalCount}/22 câu`;
    document.getElementById('matrix-total-score').textContent = `${totalScore}/10.0đ`;

    const statusBadge = document.getElementById('matrix-status-badge');
    if (p1Count === 12 && p2Count === 4 && p3Count === 6 && totalCount === 22) {
      statusBadge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 flex items-center gap-1.5';
      statusBadge.innerHTML = '<span>✓</span> Đạt chuẩn ma trận Bộ GD&ĐT (22 câu = 10đ)';
    } else {
      statusBadge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 flex items-center gap-1.5';
      statusBadge.innerHTML = `<span>⚠️</span> Chưa đủ ma trận chuẩn (${totalCount}/22 câu)`;
    }
  },

  renderQuestionsList: function() {
    const container = document.getElementById('questions-editor-list');
    container.innerHTML = '';

    if (this.currentQuestions.length === 0) {
      container.innerHTML = `
        <div class="text-center py-12 text-slate-400">
          Chưa có câu hỏi nào trong đề. Hãy chọn bài học từ Kho SGK/SBT hoặc dán nội dung để nạp.
        </div>
      `;
      return;
    }

    this.currentQuestions.forEach((q, idx) => {
      const qNum = idx + 1;
      q.number = qNum;

      const card = document.createElement('div');
      card.className = 'p-5 bg-white rounded-xl border border-slate-200 shadow-sm mb-4 relative hover:border-slate-300 transition-all';

      let detailsHtml = '';
      if (q.part === 1) {
        detailsHtml = `
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3">
            ${(q.options || []).map(opt => `
              <div class="p-2.5 rounded-lg border text-sm flex items-start gap-2 ${opt.key === q.correct_answer ? 'bg-emerald-50 border-emerald-300 font-semibold text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-800'}">
                <span class="font-bold">${opt.key}.</span>
                <span class="math-content flex-1">${opt.text}</span>
                ${opt.key === q.correct_answer ? '<span class="text-emerald-600 text-xs font-bold">✓ Đáp án đúng</span>' : ''}
              </div>
            `).join('')}
          </div>
        `;
      } else if (q.part === 2) {
        detailsHtml = `
          <div class="mt-3 space-y-2">
            ${(q.items || []).map(it => {
              const isTrue = q.correct_answers ? q.correct_answers[it.key] : true;
              return `
                <div class="p-2.5 rounded-lg border border-slate-200 bg-slate-50 text-sm flex items-center justify-between gap-3">
                  <div class="flex items-start gap-2 flex-1">
                    <span class="font-bold">${it.key})</span>
                    <span class="math-content text-slate-800">${it.text}</span>
                  </div>
                  <span class="px-2.5 py-1 rounded-md text-xs font-bold ${isTrue ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}">
                    ${isTrue ? 'Đúng' : 'Sai'}
                  </span>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else {
        detailsHtml = `
          <div class="mt-3 p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center gap-3">
            <span class="text-xs font-bold text-slate-600 uppercase">Đáp án chấp nhận:</span>
            <span class="px-3 py-1 bg-white border border-slate-300 rounded-md font-mono font-bold text-emerald-700 text-sm">
              ${q.correct_answer}
            </span>
            <span class="text-xs text-slate-400">(Tự chấp nhận cả dấu chấm . và phẩy ,)</span>
          </div>
        `;
      }

      card.innerHTML = `
        <div class="flex items-center justify-between gap-3 mb-2">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-md bg-slate-800 text-white text-xs font-bold">Câu ${qNum}</span>
            <span class="badge-part ${q.part === 1 ? 'bg-blue-100 text-blue-700' : (q.part === 2 ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800')}">
              Phần ${q.part === 1 ? 'I' : (q.part === 2 ? 'II' : 'III')}
            </span>
            <span class="text-xs text-slate-500 font-medium">(${q.points || (q.part === 1 ? 0.25 : (q.part === 2 ? 1.0 : 0.5))}đ)</span>
            <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">${q.difficulty || 'Chuẩn'}</span>
          </div>
          <button type="button" class="text-rose-500 hover:text-rose-700 text-xs font-medium" onclick="TeacherPortal.deleteQuestion(${idx})">
            ✕ Xóa câu này
          </button>
        </div>
        <div class="text-slate-900 text-sm font-normal leading-relaxed math-content whitespace-pre-line">
          ${q.stem}
        </div>
        ${detailsHtml}
        ${q.explanation ? `
          <div class="mt-3 p-3 rounded-lg bg-blue-50/70 border border-blue-100 text-xs text-blue-900">
            <span class="font-bold">Lời giải:</span> <span class="math-content whitespace-pre-line">${q.explanation}</span>
          </div>
        ` : ''}
      `;

      container.appendChild(card);
    });

    App.renderMath(container);
  },

  deleteQuestion: function(idx) {
    if (confirm(`Bạn có chắc muốn xóa câu hỏi số ${idx + 1}?`)) {
      this.currentQuestions.splice(idx, 1);
      this.renderQuestionsList();
      this.updateMatrixWidget();
    }
  },

  // --- Preview Modal ---
  openPreview: function() {
    if (this.currentQuestions.length === 0) {
      App.showToast('Chưa có câu hỏi nào để xem trước!', 'warning');
      return;
    }

    const title = document.getElementById('exam-title-input').value || 'Xem trước đề thi';
    const grade = document.getElementById('exam-grade-input').value;
    const duration = document.getElementById('exam-duration-input').value || 50;

    document.getElementById('preview-title').textContent = title;
    document.getElementById('preview-meta').textContent = `Khối ${grade} • ${duration} phút • ${this.currentQuestions.length} câu`;

    const container = document.getElementById('preview-questions-container');
    container.innerHTML = '';

    this.currentQuestions.forEach((q, idx) => {
      const card = document.createElement('div');
      card.className = 'p-5 bg-white rounded-xl border border-slate-200 mb-4 shadow-sm';
      
      let bodyHtml = '';
      if (q.part === 1) {
        bodyHtml = `
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3">
            ${(q.options || []).map(opt => `
              <div class="p-2.5 rounded-lg border border-slate-200 bg-slate-50 flex items-start gap-2 text-sm">
                <span class="font-bold min-w-[20px]">${opt.key}.</span>
                <span class="math-content flex-1">${opt.text}</span>
              </div>
            `).join('')}
          </div>
        `;
      } else if (q.part === 2) {
        bodyHtml = `
          <div class="mt-3 space-y-2">
            ${(q.items || []).map(it => `
              <div class="p-2.5 rounded-lg border border-slate-200 bg-slate-50 flex items-center justify-between text-sm">
                <div class="flex items-start gap-2 flex-1">
                  <span class="font-bold">${it.key})</span>
                  <span class="math-content">${it.text}</span>
                </div>
                <div class="flex gap-1.5">
                  <span class="px-3 py-1 rounded border bg-white text-xs font-bold text-slate-600">Đúng</span>
                  <span class="px-3 py-1 rounded border bg-white text-xs font-bold text-slate-600">Sai</span>
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else {
        bodyHtml = `
          <div class="mt-3">
            <input type="text" disabled placeholder="Nhập số (chấp nhận cả . và ,)" class="w-full max-w-xs px-3 py-2 bg-slate-100 border border-slate-300 rounded-lg text-sm" />
          </div>
        `;
      }

      card.innerHTML = `
        <div class="flex items-center gap-2 mb-2">
          <span class="px-2 py-0.5 rounded bg-slate-800 text-white font-bold text-xs">Câu ${idx + 1}</span>
          <span class="badge-part ${q.part === 1 ? 'bg-blue-100 text-blue-700' : (q.part === 2 ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700')}">
            Phần ${q.part === 1 ? 'I' : (q.part === 2 ? 'II' : 'III')}
          </span>
          <span class="text-xs text-slate-400">(${q.points || 0.25}đ)</span>
        </div>
        <div class="text-sm text-slate-900 math-content whitespace-pre-line">${q.stem}</div>
        ${bodyHtml}
      `;

      container.appendChild(card);
    });

    document.getElementById('preview-modal').classList.remove('hidden');
    App.renderMath(container);
  },

  closePreview: function() {
    document.getElementById('preview-modal').classList.add('hidden');
  },

  // --- Publish Exam ---
  publishExam: async function() {
    if (this.currentQuestions.length === 0) {
      App.showToast('Vui lòng thêm câu hỏi trước khi xuất bản!', 'warning');
      return;
    }

    const title = document.getElementById('exam-title-input').value.trim() || 'Đề kiểm tra môn Toán';
    const grade = document.getElementById('exam-grade-input').value;
    const duration = parseInt(document.getElementById('exam-duration-input').value) || 50;
    const shuffleQ = document.getElementById('exam-shuffle-q').checked;
    const shuffleOpt = document.getElementById('exam-shuffle-opt').checked;

    const payload = {
      title,
      grade,
      book: document.getElementById('curriculum-book')?.value || 'Ket_Noi_Tri_Thuc',
      chapter: document.getElementById('curriculum-chapter')?.selectedOptions[0]?.textContent || '',
      duration_minutes: duration,
      shuffle_questions: shuffleQ,
      shuffle_options: shuffleOpt,
      questions: this.currentQuestions
    };

    try {
      const res = await fetch('/api/exams', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Xuất bản thất bại!');

      const examUrl = `${window.location.origin}/exam/${data.exam_id}`;
      document.getElementById('published-link-input').value = examUrl;
      document.getElementById('publish-modal').classList.remove('hidden');

      this.loadExamsList();
      App.showToast('Đã xuất bản đề thi thành công!', 'success');
    } catch (err) {
      App.showToast(err.message, 'error');
    }
  },

  closePublishModal: function() {
    document.getElementById('publish-modal').classList.add('hidden');
  },

  copyPublishedLink: function() {
    const val = document.getElementById('published-link-input').value;
    App.copyToClipboard(val, 'Đã sao chép link đề thi gửi học sinh!');
  },

  // --- Exam Management & Results ---
  loadExamsList: async function() {
    try {
      const res = await fetch('/api/exams');
      const data = await res.json();
      const container = document.getElementById('exams-table-body');
      if (!container) return;

      container.innerHTML = '';
      const exams = data.exams || [];

      if (exams.length === 0) {
        container.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-slate-400">Chưa có đề thi nào. Hãy tạo đề mới bên cạnh!</td></tr>`;
        return;
      }

      exams.forEach(ex => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-slate-100 hover:bg-slate-50/80 transition-colors';
        const examUrl = `${window.location.origin}/exam/${ex.id}`;

        tr.innerHTML = `
          <td class="px-4 py-3 font-semibold text-slate-900">${ex.title}</td>
          <td class="px-4 py-3 text-center"><span class="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">Khối ${ex.grade}</span></td>
          <td class="px-4 py-3 text-center text-slate-600">${ex.duration_minutes} phút</td>
          <td class="px-4 py-3 text-center font-bold text-slate-800">${ex.submission_count || 0} bài</td>
          <td class="px-4 py-3 text-center font-bold ${ex.avg_score >= 8.0 ? 'text-emerald-600' : 'text-slate-700'}">${ex.avg_score ? ex.avg_score.toFixed(2) : '-'}</td>
          <td class="px-4 py-3 text-xs text-slate-500">${App.formatDate(ex.created_at)}</td>
          <td class="px-4 py-3 text-right space-x-2">
            <button class="px-3 py-1 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 text-xs font-bold" onclick="App.copyToClipboard('${examUrl}')">Copy Link</button>
            <button class="px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 text-xs font-bold" onclick="TeacherPortal.viewResults('${ex.id}', '${ex.title}')">Xem Kết Quả</button>
            <button class="px-2.5 py-1 rounded-lg text-rose-500 hover:bg-rose-50 text-xs font-bold" onclick="TeacherPortal.deleteExam('${ex.id}')">Xóa</button>
          </td>
        `;
        container.appendChild(tr);
      });
    } catch (e) {
      console.error(e);
    }
  },

  deleteExam: async function(examId) {
    if (confirm('Bạn có chắc chắn muốn xóa đề thi này và toàn bộ kết quả bài nộp của học sinh?')) {
      try {
        const res = await fetch(`/api/exams/${examId}`, { method: 'DELETE' });
        if (res.ok) {
          App.showToast('Đã xóa đề thi!', 'success');
          this.loadExamsList();
        }
      } catch (e) {
        App.showToast('Lỗi khi xóa đề!', 'error');
      }
    }
  },

  viewResults: async function(examId, examTitle) {
    this.currentResultsExamId = examId;
    document.getElementById('results-section').classList.remove('hidden');
    document.getElementById('results-exam-title').textContent = examTitle || 'Kết quả kiểm tra';
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });

    await this.loadClassFilter(examId);
    await this.fetchResultsData();
  },

  loadClassFilter: async function(examId) {
    try {
      const res = await fetch(`/api/exams/${examId}/results`);
      const data = await res.json();
      const select = document.getElementById('results-class-filter');
      select.innerHTML = '<option value="Tất cả">Tất cả các lớp</option>';

      const classes = data.classes || [];
      classes.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = `Lớp ${c}`;
        select.appendChild(opt);
      });

      this.currentClassFilter = 'Tất cả';
      select.value = 'Tất cả';
    } catch (e) {}
  },

  fetchResultsData: async function() {
    if (!this.currentResultsExamId) return;

    const classVal = document.getElementById('results-class-filter').value;
    const filterParam = classVal === 'Tất cả' ? '' : `?class_name=${encodeURIComponent(classVal)}`;

    try {
      const res = await fetch(`/api/exams/${this.currentResultsExamId}/results${filterParam}`);
      const data = await res.json();
      const subs = data.submissions || [];
      const tbody = document.getElementById('results-table-body');
      tbody.innerHTML = '';

      if (subs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" class="text-center py-8 text-slate-400">Chưa có học sinh nào nộp bài cho bộ lọc này.</td></tr>`;
        return;
      }

      subs.forEach((sub, idx) => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-slate-100 hover:bg-slate-50 transition-colors';

        const hasCheated = sub.tab_switch_count > 0;
        const totalSc = parseFloat(sub.total_score).toFixed(2);
        const spentMin = Math.floor(sub.time_spent_seconds / 60);
        const spentSec = sub.time_spent_seconds % 60;

        tr.innerHTML = `
          <td class="px-4 py-3 text-center text-slate-500">${idx + 1}</td>
          <td class="px-4 py-3 font-bold text-slate-900">${sub.student_name}</td>
          <td class="px-4 py-3 text-center"><span class="px-2 py-0.5 rounded bg-slate-100 font-bold text-xs">${sub.student_class}</span></td>
          <td class="px-4 py-3 text-center font-medium">${parseFloat(sub.part1_score).toFixed(2)}</td>
          <td class="px-4 py-3 text-center font-medium">${parseFloat(sub.part2_score).toFixed(2)}</td>
          <td class="px-4 py-3 text-center font-medium">${parseFloat(sub.part3_score).toFixed(2)}</td>
          <td class="px-4 py-3 text-center font-extrabold text-base ${sub.total_score >= 8.0 ? 'text-emerald-600' : 'text-blue-600'}">${totalSc}</td>
          <td class="px-4 py-3 text-center text-xs text-slate-600">${spentMin}p ${spentSec}s</td>
          <td class="px-4 py-3 text-center">
            ${hasCheated ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-700 flex items-center justify-center gap-1">⚠️ ${sub.tab_switch_count} lần</span>` : `<span class="text-xs text-emerald-600 font-semibold">✓ 0</span>`}
          </td>
          <td class="px-4 py-3 text-center text-xs text-slate-500">${App.formatDate(sub.submit_time)}</td>
        `;
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.error(err);
    }
  },

  exportExcel: function() {
    if (!this.currentResultsExamId) {
      App.showToast('Vui lòng chọn đề thi để xuất kết quả!', 'warning');
      return;
    }
    const classVal = document.getElementById('results-class-filter').value;
    const url = `/api/exams/${this.currentResultsExamId}/export-excel?class_name=${encodeURIComponent(classVal)}`;
    App.showToast('Đang tạo file Excel...', 'info');
    window.location.href = url;
  },

  // --- Tab Navigation ---
  switchTab: function(tabId) {
    document.querySelectorAll('.teacher-tab-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.teacher-tab-btn').forEach(btn => {
      btn.classList.remove('bg-blue-600', 'text-white');
      btn.classList.add('bg-white', 'text-slate-700');
    });

    const activeContent = document.getElementById(`tab-content-${tabId}`);
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);

    if (activeContent) activeContent.classList.remove('hidden');
    if (activeBtn) {
      activeBtn.classList.remove('bg-white', 'text-slate-700');
      activeBtn.classList.add('bg-blue-600', 'text-white');
    }
  },

  bindEvents: function() {
    const classFilter = document.getElementById('results-class-filter');
    if (classFilter) {
      classFilter.addEventListener('change', () => this.fetchResultsData());
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  TeacherPortal.init();
});
