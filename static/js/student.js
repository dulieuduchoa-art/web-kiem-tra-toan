/**
 * Student Examination Room Logic
 * - Countdown timer with auto-submit
 * - Anti-cheat tab switch / blur detection
 * - KaTeX formula rendering
 * - Question palette navigation
 * - Ministry of Education 3-part responsive UI
 */

const StudentExam = {
  examId: null,
  examData: null,
  studentName: '',
  studentClass: '',
  startTime: null,
  timeSpentSeconds: 0,
  tabSwitchCount: 0,
  remainingSeconds: 0,
  timerInterval: null,
  answers: {}, // { [qId]: choice / {a: true, b: false} / "number_str" }
  isSubmitted: false,

  init: function() {
    // Extract exam ID from URL pathname /exam/{id}
    const pathParts = window.location.pathname.split('/');
    this.examId = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2];
    
    if (!this.examId) {
      alert('Không tìm thấy mã đề thi!');
      window.location.href = '/';
      return;
    }

    this.loadExamData();
    this.bindEvents();
  },

  loadExamData: async function() {
    try {
      const res = await fetch(`/api/exams/${this.examId}?mode=student`);
      if (!res.ok) {
        throw new Error('Đề thi không tồn tại hoặc đã bị gỡ!');
      }
      this.examData = await res.json();
      this.renderStartScreen();
    } catch (err) {
      document.getElementById('loading-state').innerHTML = `
        <div class="text-center p-8 bg-white rounded-2xl shadow-sm border border-rose-200">
          <div class="text-4xl mb-3">⚠️</div>
          <h2 class="text-xl font-bold text-slate-800 mb-2">Không thể tải đề thi</h2>
          <p class="text-slate-600 mb-4">${err.message}</p>
          <a href="/" class="inline-block px-5 py-2.5 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700">Về trang chủ</a>
        </div>
      `;
    }
  },

  renderStartScreen: function() {
    document.getElementById('loading-state').classList.add('hidden');
    document.getElementById('start-screen').classList.remove('hidden');

    document.getElementById('exam-title-display').textContent = this.examData.title;
    document.getElementById('exam-grade-badge').textContent = `Khối ${this.examData.grade}`;
    document.getElementById('exam-duration-display').textContent = `${this.examData.duration_minutes} phút`;
    document.getElementById('exam-qcount-display').textContent = `${this.examData.questions.length} câu`;

    // Check if previous incomplete session exists in localStorage
    const saved = localStorage.getItem(`math_exam_session_${this.examId}`);
    if (saved) {
      try {
        const session = JSON.parse(saved);
        if (session.studentName) {
          document.getElementById('student-name-input').value = session.studentName;
        }
        if (session.studentClass) {
          document.getElementById('student-class-input').value = session.studentClass;
        }
      } catch (e) {}
    }
  },

  startExam: function() {
    const nameInput = document.getElementById('student-name-input').value.trim();
    const classInput = document.getElementById('student-class-input').value.trim();

    if (!nameInput) {
      App.showToast('Vui lòng nhập Họ và tên!', 'warning');
      document.getElementById('student-name-input').focus();
      return;
    }
    if (!classInput) {
      App.showToast('Vui lòng nhập Lớp học!', 'warning');
      document.getElementById('student-class-input').focus();
      return;
    }

    this.studentName = nameInput;
    this.studentClass = classInput;
    this.startTime = new Date().toISOString();

    // Check saved answers
    const saved = localStorage.getItem(`math_exam_session_${this.examId}`);
    if (saved) {
      try {
        const session = JSON.parse(saved);
        if (session.studentName === this.studentName && session.answers) {
          this.answers = session.answers;
          this.tabSwitchCount = session.tabSwitchCount || 0;
        }
      } catch (e) {}
    }

    this.remainingSeconds = (this.examData.duration_minutes || 50) * 60;

    // Switch UI
    document.getElementById('start-screen').classList.add('hidden');
    document.getElementById('exam-active-screen').classList.remove('hidden');

    // Setup sticky header
    document.getElementById('active-exam-title').textContent = this.examData.title;
    document.getElementById('active-student-info').textContent = `${this.studentName} - Lớp ${this.studentClass}`;

    this.renderQuestions();
    this.renderPalette();
    this.startTimer();
    this.setupAntiCheat();

    // Render KaTeX
    App.renderMath(document.getElementById('questions-container'));
  },

  renderPalette: function() {
    const p1Container = document.getElementById('palette-part1');
    const p2Container = document.getElementById('palette-part2');
    const p3Container = document.getElementById('palette-part3');

    p1Container.innerHTML = '';
    p2Container.innerHTML = '';
    p3Container.innerHTML = '';

    this.examData.questions.forEach((q, idx) => {
      const pill = document.createElement('button');
      pill.type = 'button';
      pill.id = `palette_pill_${q.id}`;
      pill.className = `q-pill ${this.isQuestionAnswered(q) ? 'answered' : 'unanswered'}`;
      pill.textContent = q.number || (idx + 1);
      pill.onclick = () => this.scrollToQuestion(q.id);

      if (q.part === 1) p1Container.appendChild(pill);
      else if (q.part === 2) p2Container.appendChild(pill);
      else p3Container.appendChild(pill);
    });

    this.updateAnsweredCount();
  },

  renderQuestions: function() {
    const container = document.getElementById('questions-container');
    container.innerHTML = '';

    let currentPart = null;

    this.examData.questions.forEach((q, idx) => {
      // If new part, insert part header banner
      if (q.part !== currentPart) {
        currentPart = q.part;
        const banner = document.createElement('div');
        banner.className = 'my-8 p-4 rounded-2xl border shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-2';
        
        if (currentPart === 1) {
          banner.className += ' bg-blue-50 border-blue-200 text-blue-900';
          banner.innerHTML = `
            <div>
              <span class="badge-part bg-blue-600 text-white mr-2">PHẦN I</span>
              <span class="font-bold text-lg">CÂU TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN</span>
            </div>
            <div class="text-sm font-medium text-blue-700">12 câu • 0,25 điểm/câu • Tổng 3,0 điểm</div>
          `;
        } else if (currentPart === 2) {
          banner.className += ' bg-amber-50 border-amber-200 text-amber-900';
          banner.innerHTML = `
            <div>
              <span class="badge-part bg-amber-600 text-white mr-2">PHẦN II</span>
              <span class="font-bold text-lg">CÂU TRẮC NGHIỆM ĐÚNG / SAI</span>
            </div>
            <div class="text-sm font-medium text-amber-800">4 câu • 1,0 điểm/câu • Chấm lũy tiến (1 ý: 0,1đ | 2 ý: 0,25đ | 3 ý: 0,5đ | 4 ý: 1,0đ)</div>
          `;
        } else {
          banner.className += ' bg-emerald-50 border-emerald-200 text-emerald-900';
          banner.innerHTML = `
            <div>
              <span class="badge-part bg-emerald-600 text-white mr-2">PHẦN III</span>
              <span class="font-bold text-lg">CÂU TRẮC NGHIỆM TRẢ LỜI NGẮN</span>
            </div>
            <div class="text-sm font-medium text-emerald-800">6 câu • 0,5 điểm/câu • Tổng 3,0 điểm (Hệ thống chấp nhận cả dấu . và ,)</div>
          `;
        }
        container.appendChild(banner);
      }

      // Question card
      const card = document.createElement('div');
      card.id = `q_card_${q.id}`;
      card.className = 'p-6 bg-white rounded-2xl shadow-sm border border-slate-200 mb-6 transition-all duration-200';

      const diffBadgeColors = {
        'Dễ': 'bg-slate-100 text-slate-700',
        'Trung bình': 'bg-blue-100 text-blue-700',
        'Khó': 'bg-orange-100 text-orange-700',
        'Cực khó': 'bg-rose-100 text-rose-700'
      };
      const diffColor = diffBadgeColors[q.difficulty] || 'bg-slate-100 text-slate-700';

      let bodyHtml = '';

      // --- Part 1 HTML ---
      if (q.part === 1) {
        const savedChoice = this.answers[q.id] || null;
        bodyHtml = `
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
            ${(q.options || []).map(opt => `
              <div class="option-card flex items-start gap-3 p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 ${savedChoice === opt.key ? 'selected' : ''}"
                   onclick="StudentExam.selectPart1Option('${q.id}', '${opt.key}', this)">
                <span class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm ${savedChoice === opt.key ? 'bg-blue-600 text-white' : 'bg-white text-slate-700 border border-slate-300'}">
                  ${opt.key}
                </span>
                <div class="flex-1 text-slate-800 text-base math-content pt-0.5">
                  ${opt.text}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } 
      // --- Part 2 HTML ---
      else if (q.part === 2) {
        const savedMap = this.answers[q.id] || {};
        bodyHtml = `
          <div class="mt-4 space-y-3">
            <div class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">Mỗi ý chọn Đúng hoặc Sai:</div>
            ${(q.items || []).map(it => {
              const userVal = savedMap[it.key];
              return `
                <div class="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 gap-3">
                  <div class="flex items-start gap-2.5 flex-1">
                    <span class="font-bold text-slate-700 min-w-[20px]">${it.key})</span>
                    <span class="text-slate-800 text-base math-content flex-1">${it.text}</span>
                  </div>
                  <div class="flex items-center gap-2 self-end sm:self-center">
                    <button type="button" 
                            class="btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm ${userVal === true ? 'active-true' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'}"
                            onclick="StudentExam.selectPart2Choice('${q.id}', '${it.key}', true, this)">
                      Đúng
                    </button>
                    <button type="button" 
                            class="btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm ${userVal === false ? 'active-false' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'}"
                            onclick="StudentExam.selectPart2Choice('${q.id}', '${it.key}', false, this)">
                      Sai
                    </button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } 
      // --- Part 3 HTML ---
      else {
        const savedVal = this.answers[q.id] || '';
        bodyHtml = `
          <div class="mt-4 max-w-md">
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">
              Nhập câu trả lời (số thập phân dùng dấu chấm . hoặc phẩy ,):
            </label>
            <div class="relative">
              <input type="text" 
                     id="input_q_${q.id}"
                     value="${savedVal}"
                     placeholder="Ví dụ: 3.5 hoặc 3,5 hoặc -4"
                     class="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-lg font-bold text-slate-800 focus:outline-none focus:border-emerald-600 focus:bg-white focus:ring-2 focus:ring-emerald-100 transition-all"
                     oninput="StudentExam.handlePart3Input('${q.id}', this.value)" />
              <div class="absolute right-3 top-3.5 text-xs text-slate-400 font-medium">Nhập số</div>
            </div>
          </div>
        `;
      }

      card.innerHTML = `
        <div class="flex items-start justify-between gap-4 mb-3">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-white font-bold text-sm">Câu ${q.number || (idx + 1)}</span>
            <span class="px-2 py-0.5 rounded text-xs font-semibold ${diffColor}">${q.difficulty || 'Chuẩn'}</span>
            <span class="text-xs text-slate-500 font-medium">(${q.points} điểm)</span>
          </div>
          <button type="button" class="text-xs text-slate-400 hover:text-slate-600" onclick="StudentExam.scrollToTop()">↑ Lên đầu</button>
        </div>
        <div class="text-slate-900 text-base leading-relaxed math-content font-normal whitespace-pre-line">
          ${q.stem}
        </div>
        ${bodyHtml}
      `;

      container.appendChild(card);
    });
  },

  // Part 1 Option Click
  selectPart1Option: function(qId, key, cardElem) {
    this.answers[qId] = key;
    
    // Update card styling
    const parent = cardElem.parentElement;
    parent.querySelectorAll('.option-card').forEach(c => {
      c.classList.remove('selected');
      const badge = c.querySelector('span');
      badge.className = 'flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm bg-white text-slate-700 border border-slate-300';
    });

    cardElem.classList.add('selected');
    const activeBadge = cardElem.querySelector('span');
    activeBadge.className = 'flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm bg-blue-600 text-white';

    this.onAnswerChanged(qId);
  },

  // Part 2 True/False Click
  selectPart2Choice: function(qId, itemKey, isTrue, btnElem) {
    if (!this.answers[qId] || typeof this.answers[qId] !== 'object') {
      this.answers[qId] = {};
    }
    this.answers[qId][itemKey] = isTrue;

    // Toggle button styles
    const btnGroup = btnElem.parentElement;
    const trueBtn = btnGroup.children[0];
    const falseBtn = btnGroup.children[1];

    if (isTrue) {
      trueBtn.className = 'btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm active-true';
      falseBtn.className = 'btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm bg-white text-slate-700 border-slate-300 hover:bg-slate-100';
    } else {
      trueBtn.className = 'btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm bg-white text-slate-700 border-slate-300 hover:bg-slate-100';
      falseBtn.className = 'btn-tf px-4 py-1.5 rounded-lg border font-bold text-sm active-false';
    }

    this.onAnswerChanged(qId);
  },

  // Part 3 Short Answer Input
  handlePart3Input: function(qId, value) {
    const trimmed = value.trim();
    if (trimmed) {
      this.answers[qId] = trimmed;
    } else {
      delete this.answers[qId];
    }
    this.onAnswerChanged(qId);
  },

  onAnswerChanged: function(qId) {
    // Update question palette pill
    const q = this.examData.questions.find(item => item.id == qId);
    if (q) {
      const pill = document.getElementById(`palette_pill_${qId}`);
      if (pill) {
        if (this.isQuestionAnswered(q)) {
          pill.className = 'q-pill answered';
        } else {
          pill.className = 'q-pill unanswered';
        }
      }
    }

    this.updateAnsweredCount();
    this.saveSession();
  },

  isQuestionAnswered: function(q) {
    const val = this.answers[q.id];
    if (val === undefined || val === null) return false;
    
    if (q.part === 1) {
      return Boolean(val);
    } else if (q.part === 2) {
      if (typeof val !== 'object') return false;
      // All 4 sub-items must be chosen to be fully answered
      const keys = ['a', 'b', 'c', 'd'];
      return keys.every(k => val[k] !== undefined && val[k] !== null);
    } else {
      return String(val).trim().length > 0;
    }
  },

  updateAnsweredCount: function() {
    let answered = 0;
    const total = this.examData.questions.length;
    this.examData.questions.forEach(q => {
      if (this.isQuestionAnswered(q)) answered++;
    });

    const badge = document.getElementById('answered-count-badge');
    if (badge) {
      badge.textContent = `${answered}/${total}`;
    }
  },

  saveSession: function() {
    try {
      const session = {
        studentName: this.studentName,
        studentClass: this.studentClass,
        answers: this.answers,
        tabSwitchCount: this.tabSwitchCount,
        timestamp: Date.now()
      };
      localStorage.setItem(`math_exam_session_${this.examId}`, JSON.stringify(session));
    } catch (e) {}
  },

  // --- Countdown Timer ---
  startTimer: function() {
    const timerDisplay = document.getElementById('countdown-timer');
    const timerCard = document.getElementById('timer-card');

    const updateTimerUI = () => {
      this.timeSpentSeconds++;
      this.remainingSeconds--;

      if (this.remainingSeconds <= 0) {
        clearInterval(this.timerInterval);
        timerDisplay.textContent = '00:00';
        App.showToast('Hết giờ làm bài! Hệ thống đang tự động nộp bài...', 'warning', 5000);
        this.submitExam(true);
        return;
      }

      timerDisplay.textContent = App.formatTime(this.remainingSeconds);

      // Color warning when <= 5 mins (300 sec)
      if (this.remainingSeconds <= 60) {
        timerCard.classList.add('timer-warning');
      } else if (this.remainingSeconds <= 300) {
        timerCard.classList.add('bg-amber-50', 'text-amber-700', 'border-amber-300');
        timerCard.classList.remove('bg-slate-50', 'text-slate-800');
      }
    };

    updateTimerUI();
    this.timerInterval = setInterval(updateTimerUI, 1000);
  },

  // --- Anti-cheat & Tab Switch Detection ---
  setupAntiCheat: function() {
    const handleSwitch = () => {
      if (this.isSubmitted) return;
      this.tabSwitchCount++;
      this.saveSession();

      // Show alert modal
      document.getElementById('anti-cheat-modal').classList.remove('hidden');
      document.getElementById('tab-switch-count-display').textContent = this.tabSwitchCount;
    };

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        handleSwitch();
      }
    });

    window.addEventListener('blur', () => {
      handleSwitch();
    });
  },

  closeAntiCheatModal: function() {
    document.getElementById('anti-cheat-modal').classList.add('hidden');
  },

  // --- Navigation Helpers ---
  scrollToQuestion: function(qId) {
    const el = document.getElementById(`q_card_${qId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.add('ring-2', 'ring-blue-500', 'ring-offset-2');
      setTimeout(() => el.classList.remove('ring-2', 'ring-blue-500', 'ring-offset-2'), 1200);
    }
  },

  scrollToTop: function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  // --- Submit Dialog & Execution ---
  promptSubmit: function() {
    let answered = 0;
    const total = this.examData.questions.length;
    this.examData.questions.forEach(q => {
      if (this.isQuestionAnswered(q)) answered++;
    });

    const unanswered = total - answered;
    document.getElementById('submit-modal-answered').textContent = `${answered}/${total}`;
    document.getElementById('submit-modal-unanswered').textContent = unanswered;

    if (unanswered > 0) {
      document.getElementById('submit-modal-warning').classList.remove('hidden');
    } else {
      document.getElementById('submit-modal-warning').classList.add('hidden');
    }

    document.getElementById('submit-confirm-modal').classList.remove('hidden');
  },

  cancelSubmit: function() {
    document.getElementById('submit-confirm-modal').classList.add('hidden');
  },

  submitExam: async function(auto = false) {
    if (this.isSubmitted) return;
    this.isSubmitted = true;
    clearInterval(this.timerInterval);

    document.getElementById('submit-confirm-modal').classList.add('hidden');

    // Show loading overlay
    const overlay = document.getElementById('submitting-overlay');
    if (overlay) overlay.classList.remove('hidden');

    try {
      const payload = {
        student_name: this.studentName,
        student_class: this.studentClass,
        start_time: this.startTime,
        time_spent_seconds: this.timeSpentSeconds,
        tab_switch_count: this.tabSwitchCount,
        answers: this.answers
      };

      const res = await fetch(`/api/exams/${this.examId}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Nộp bài thất bại!');
      }

      const result = await res.json();
      
      // Clear session from localStorage
      localStorage.removeItem(`math_exam_session_${this.examId}`);

      // Redirect to detailed result page
      window.location.href = `/result/${result.submission_id}`;
    } catch (err) {
      this.isSubmitted = false;
      if (overlay) overlay.classList.add('hidden');
      alert(`Lỗi: ${err.message}`);
    }
  },

  bindEvents: function() {
    // Mobile palette toggle
    const toggleBtn = document.getElementById('mobile-palette-toggle');
    const drawer = document.getElementById('question-palette-drawer');
    if (toggleBtn && drawer) {
      toggleBtn.addEventListener('click', () => {
        drawer.classList.toggle('hidden');
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  StudentExam.init();
});
