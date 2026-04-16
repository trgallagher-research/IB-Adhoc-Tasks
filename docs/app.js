/* ===================================================
   Melbourne Metrics — Prototype Sketches
   Main JavaScript file.
   Handles tab switching, assessor tabs, and Chart.js
   dashboard charts for Sketch 5.
   =================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* -------------------------------------------------
     1. Main sketch tab navigation
     ------------------------------------------------- */
  var tabButtons = document.querySelectorAll('.tab-btn');
  var tabPanels = document.querySelectorAll('.tab-panel');

  tabButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      // Deactivate all
      tabButtons.forEach(function (b) { b.classList.remove('active'); });
      tabPanels.forEach(function (p) { p.classList.remove('active'); });
      // Activate clicked
      btn.classList.add('active');
      var target = document.getElementById(btn.dataset.tab);
      if (target) {
        target.classList.add('active');
      }
      // Initialise charts if switching to sketch 5 for the first time
      if (btn.dataset.tab === 'sketch5' && !chartsInitialised) {
        initDashboardCharts();
        chartsInitialised = true;
      }
    });
  });

  /* -------------------------------------------------
     2. Assessor role tabs (Sketch 2)
     ------------------------------------------------- */
  var assessorTabs = document.querySelectorAll('.assessor-tab');
  var assessorSelect = document.getElementById('assessorRoleSelect');

  assessorTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      assessorTabs.forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      // Update the dropdown in the form header to match
      if (assessorSelect) {
        assessorSelect.value = tab.dataset.role;
      }
    });
  });

  /* -------------------------------------------------
     3. Chart.js — Wellbeing Dashboard (Sketch 5)
     ------------------------------------------------- */
  var chartsInitialised = false;

  function initDashboardCharts() {

    // Shared defaults
    Chart.defaults.font.family = "'Open Sans', Arial, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#52525b';

    /* --- Panel 1: Time on MM Activities --- */
    var weeks = [];
    for (var w = 1; w <= 20; w++) { weeks.push('Wk ' + w); }

    // Sample data — gradual increase with some variation
    var evidenceCapture = [1.2,1.3,1.5,1.4,1.8,2.0,2.1,2.3,2.5,2.4,2.7,2.9,3.1,3.3,3.5,3.4,3.7,3.9,4.1,4.3];
    var judgement =       [0.8,0.9,0.9,1.0,1.1,1.2,1.4,1.5,1.6,1.8,1.9,2.0,2.1,2.3,2.4,2.5,2.7,2.8,3.0,3.1];
    var admin =           [0.5,0.5,0.6,0.6,0.7,0.7,0.8,0.8,0.9,0.9,1.0,1.0,1.1,1.1,1.2,1.2,1.3,1.3,1.4,1.5];

    // Compute total for threshold checking
    var totalHours = evidenceCapture.map(function (v, i) { return v + judgement[i] + admin[i]; });

    new Chart(document.getElementById('chartTime'), {
      type: 'line',
      data: {
        labels: weeks,
        datasets: [
          {
            label: 'Evidence capture',
            data: evidenceCapture,
            borderColor: '#1d4ed8',
            backgroundColor: 'rgba(29,78,216,.1)',
            tension: 0.3,
            fill: false,
            pointRadius: 2
          },
          {
            label: 'Judgement & moderation',
            data: judgement,
            borderColor: '#7c3aed',
            backgroundColor: 'rgba(124,58,237,.1)',
            tension: 0.3,
            fill: false,
            pointRadius: 2
          },
          {
            label: 'Administration',
            data: admin,
            borderColor: '#64748b',
            backgroundColor: 'rgba(100,116,139,.1)',
            tension: 0.3,
            fill: false,
            pointRadius: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            min: 0,
            max: 8,
            title: { display: true, text: 'Hours / week' }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              amber: {
                type: 'line',
                yMin: 5,
                yMax: 5,
                borderColor: '#f59e0b',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Amber (5 hrs)', position: 'start', font: { size: 10 } }
              },
              red: {
                type: 'line',
                yMin: 7,
                yMax: 7,
                borderColor: '#dc2626',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Red (7 hrs)', position: 'start', font: { size: 10 } }
              }
            }
          }
        }
      }
    });

    /* --- Panel 2: Perceived Workload Burden --- */
    var terms = ['Term 1 2025', 'Term 2 2025', 'Term 3 2025', 'Term 4 2025'];

    new Chart(document.getElementById('chartWorkload'), {
      type: 'bar',
      data: {
        labels: terms,
        datasets: [
          {
            label: 'Classroom teacher',
            data: [2.1, 2.6, 3.0, 3.4],
            backgroundColor: '#60a5fa'
          },
          {
            label: 'Coordinator',
            data: [2.8, 3.2, 3.6, 3.9],
            backgroundColor: '#1d4ed8'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            min: 0,
            max: 5,
            title: { display: true, text: 'Perceived burden (1-5 scale)' },
            ticks: {
              callback: function (value) {
                var labels = { 1: '1 — Very manageable', 2: '2', 3: '3', 4: '4', 5: '5 — Unsustainable' };
                return labels[value] || value;
              }
            }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              amber: {
                type: 'line',
                yMin: 3.5,
                yMax: 3.5,
                borderColor: '#f59e0b',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Amber', position: 'start', font: { size: 10 } }
              },
              red: {
                type: 'line',
                yMin: 4.0,
                yMax: 4.0,
                borderColor: '#dc2626',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Red', position: 'start', font: { size: 10 } }
              }
            }
          }
        }
      }
    });

    /* --- Panel 3: Teacher Wellbeing Index --- */
    new Chart(document.getElementById('chartWellbeing'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          {
            label: 'Wellbeing Index',
            data: [74, 68, 63, 58],
            borderColor: '#16a34a',
            backgroundColor: 'rgba(22,163,74,.1)',
            tension: 0.3,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: '#16a34a'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            min: 0,
            max: 100,
            title: { display: true, text: 'Composite score (0–100)' }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              amber: {
                type: 'line',
                yMin: 60,
                yMax: 60,
                borderColor: '#f59e0b',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Amber (60)', position: 'start', font: { size: 10 } }
              },
              red: {
                type: 'line',
                yMin: 50,
                yMax: 50,
                borderColor: '#dc2626',
                borderWidth: 2,
                borderDash: [6, 4],
                label: { display: true, content: 'Red (50)', position: 'start', font: { size: 10 } }
              }
            }
          }
        }
      }
    });
  }
});
