/**
 * Shared Application Utilities for Math Exam System
 * Includes KaTeX math rendering, toast notifications, and helpers.
 */

window.App = {
  // Render LaTeX formulas using KaTeX
  renderMath: function(element) {
    const target = element || document.body;
    if (window.renderMathInElement) {
      window.renderMathInElement(target, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false },
          { left: '\\[', right: '\\]', display: true }
        ],
        throwOnError: false,
        output: 'htmlAndMathml'
      });
    }
  },

  // Toast Notification
  showToast: function(message, type = 'info', duration = 3500) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const colors = {
      success: 'bg-emerald-600 text-white',
      error: 'bg-rose-600 text-white',
      warning: 'bg-amber-600 text-white',
      info: 'bg-blue-600 text-white'
    };
    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠️',
      info: 'ℹ'
    };

    const colorClass = colors[type] || colors.info;
    const icon = icons[type] || icons.info;

    toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg font-medium text-sm transition-all transform duration-300 translate-y-2 opacity-0 ${colorClass}`;
    toast.innerHTML = `
      <span class="text-base font-bold">${icon}</span>
      <span class="flex-1">${message}</span>
      <button class="ml-2 opacity-70 hover:opacity-100 text-white" onclick="this.parentElement.remove()">✕</button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);

    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  // Copy text to clipboard
  copyToClipboard: function(text, successMsg = 'Đã sao chép liên kết vào bộ nhớ tạm!') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        App.showToast(successMsg, 'success');
      }).catch(() => {
        App.fallbackCopyText(text, successMsg);
      });
    } else {
      App.fallbackCopyText(text, successMsg);
    }
  },

  fallbackCopyText: function(text, successMsg) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      App.showToast(successMsg, 'success');
    } catch (err) {
      App.showToast('Không thể sao chép tự động!', 'error');
    }
    document.body.removeChild(textarea);
  },

  // Format seconds to mm:ss
  formatTime: function(totalSeconds) {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  },

  // Format datetime
  formatDate: function(isoString) {
    if (!isoString) return '';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return isoString;
    }
  }
};
