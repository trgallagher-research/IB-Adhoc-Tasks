/* ===================================================
   Melbourne Metrics — Prototype Sketches
   View router, assessor tabs, dashboard charts.
   =================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* -------------------------------------------------
     1. View router: landing ↔ per-problem views
     Only one <section class="view"> is visible at
     a time. URL hash drives which view is shown.
     ------------------------------------------------- */
  var views = document.querySelectorAll('.view');
  var tiles = document.querySelectorAll('.problem-tile');
  var backLinks = document.querySelectorAll('.back-link');

  /* Map hash → view ID */
  var hashToViewId = {
    '': 'landing',
    '#': 'landing',
    '#landing': 'landing',
    '#problem-1': 'view-problem-1',
    '#problem-2': 'view-problem-2',
    '#problem-3': 'view-problem-3',
    '#problem-4': 'view-problem-4'
  };

  /* Inverse: view ID → hash (for writing back to URL) */
  var viewIdToHash = {
    'landing': '',
    'view-problem-1': '#problem-1',
    'view-problem-2': '#problem-2',
    'view-problem-3': '#problem-3',
    'view-problem-4': '#problem-4'
  };

  function showView(viewId) {
    views.forEach(function (v) { v.classList.remove('view-active'); });
    var target = document.getElementById(viewId);
    if (target) {
      target.classList.add('view-active');
    } else {
      document.getElementById('landing').classList.add('view-active');
    }
    // Reset scroll to the top of the page
    window.scrollTo({ top: 0, behavior: 'instant' });
    // Initialise charts lazily the first time Problem 2 view opens
    if (viewId === 'view-problem-2' && !chartsInitialised) {
      initDashboardCharts();
      chartsInitialised = true;
    }
  }

  function handleHashChange() {
    var hash = window.location.hash;
    var viewId = hashToViewId[hash] || 'landing';
    showView(viewId);
  }

  /* Tile clicks: set hash (which triggers hashchange) */
  tiles.forEach(function (tile) {
    tile.addEventListener('click', function (e) {
      e.preventDefault();
      var viewId = tile.dataset.view;
      window.location.hash = viewIdToHash[viewId] || '';
      // If hash did not change (already on it), still trigger view switch
      if (!window.location.hash && viewId === 'landing') {
        showView('landing');
      }
    });
  });

  /* Back links: return to landing */
  backLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      window.location.hash = '';
      // Some browsers clear history hash without firing hashchange; force it
      showView('landing');
    });
  });

  /* React to manual hash navigation (bookmarks, back/forward) */
  window.addEventListener('hashchange', handleHashChange);

  /* Initial view on page load */
  handleHashChange();

  /* -------------------------------------------------
     2. Assessor role tabs (Sketch 2)
     ------------------------------------------------- */
  var assessorTabs = document.querySelectorAll('.assessor-tab');
  var assessorSelect = document.getElementById('assessorRoleSelect');

  assessorTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      assessorTabs.forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      if (assessorSelect) {
        assessorSelect.value = tab.dataset.role;
      }
    });
  });

  /* -------------------------------------------------
     3. Chart.js — Wellbeing & Sustainability Dashboard
     Multi-school comparison with realistic data.
     Initialises lazily on first Problem 2 view.
     ------------------------------------------------- */
  var chartsInitialised = false;

  function initDashboardCharts() {

    Chart.defaults.font.family = "'Open Sans', Arial, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#52525b';

    var terms = ['T1 2025', 'T2 2025', 'T3 2025', 'T4 2025', 'T1 2026', 'T2 2026'];

    var colours = {
      greenfield: '#1d4ed8',
      riverside:  '#059669',
      summit:     '#dc2626',
      horizon:    '#7c3aed',
      cohort:     '#64748b'
    };

    /* Activity volume (Ruby telemetry) */
    new Chart(document.getElementById('chartActivity'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', [4.2, 5.1, 6.3, 5.8, 5.4, 6.0], colours.greenfield),
          makeDataset('Riverside Academy',        [2.8, 5.2, 8.1, 9.8, 8.4, 7.6], colours.riverside),
          makeDataset('Summit International',     [6.4, 8.2, 11.5, 13.8, 15.2, 16.4], colours.summit),
          makeDataset('Horizon College',          [3.6, 4.2, 5.8, 6.4, 6.1, 6.5], colours.horizon),
          makeCohortDataset('Cohort average',     [4.3, 5.7, 7.9, 8.9, 8.8, 9.1], colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: { min: 0, max: 20, title: { display: true, text: 'Evidence items per teacher per month' } }
        }
      }
    });

    /* Perceived time investment */
    new Chart(document.getElementById('chartTime'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', [2.3, 2.5, 2.6, 2.4, 2.5, 2.6], colours.greenfield),
          makeDataset('Riverside Academy',        [2.8, 3.4, 4.0, 3.8, 3.6, 3.5], colours.riverside),
          makeDataset('Summit International',     [3.2, 3.8, 4.1, 4.3, 4.5, 4.6], colours.summit),
          makeDataset('Horizon College',          [2.4, 2.7, 2.9, 3.0, 2.9, 3.0], colours.horizon),
          makeCohortDataset('Cohort average',     [2.7, 3.1, 3.4, 3.4, 3.4, 3.4], colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: { min: 1, max: 5, title: { display: true, text: 'Likert (1 none → 5 very heavy)' } }
        }
      }
    });

    /* Perceived workload burden */
    new Chart(document.getElementById('chartWorkload'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', [2.1, 2.3, 2.4, 2.3, 2.3, 2.4], colours.greenfield),
          makeDataset('Riverside Academy',        [2.5, 2.9, 3.6, 3.8, 3.3, 3.2], colours.riverside),
          makeDataset('Summit International',     [2.9, 3.4, 3.8, 4.1, 4.3, 4.4], colours.summit),
          makeDataset('Horizon College',          [2.3, 2.5, 2.7, 2.8, 2.7, 2.8], colours.horizon),
          makeCohortDataset('Cohort average',     [2.5, 2.8, 3.1, 3.3, 3.2, 3.2], colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: { min: 1, max: 5, title: { display: true, text: 'Likert (1 very manageable → 5 unsustainable)' } }
        },
        plugins: {
          annotation: {
            annotations: {
              amber: {
                type: 'line', yMin: 3.5, yMax: 3.5,
                borderColor: '#f59e0b', borderWidth: 1.5, borderDash: [5, 4],
                label: { display: true, content: 'Amber (3.5)', position: 'start', font: { size: 10 }, backgroundColor: 'rgba(254,243,199,.9)', color: '#78350f' }
              },
              red: {
                type: 'line', yMin: 4.0, yMax: 4.0,
                borderColor: '#dc2626', borderWidth: 1.5, borderDash: [5, 4],
                label: { display: true, content: 'Red (4.0)', position: 'start', font: { size: 10 }, backgroundColor: 'rgba(254,226,226,.9)', color: '#991b1b' }
              }
            }
          }
        }
      }
    });

    /* WHO-5 Wellbeing Index */
    new Chart(document.getElementById('chartWellbeing'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', [72, 70, 71, 73, 72, 71], colours.greenfield),
          makeDataset('Riverside Academy',        [68, 65, 58, 55, 62, 64], colours.riverside),
          makeDataset('Summit International',     [66, 62, 56, 50, 47, 45], colours.summit),
          makeDataset('Horizon College',          [70, 69, 67, 68, 67, 68], colours.horizon),
          makeCohortDataset('Cohort average',     [69, 66, 63, 61, 62, 62], colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: { min: 30, max: 100, title: { display: true, text: 'WHO-5 Wellbeing Index (0–100)' } }
        },
        plugins: {
          annotation: {
            annotations: {
              who5Threshold: {
                type: 'line', yMin: 50, yMax: 50,
                borderColor: '#dc2626', borderWidth: 1.5, borderDash: [5, 4],
                label: { display: true, content: 'WHO-5 threshold (50)', position: 'start', font: { size: 10 }, backgroundColor: 'rgba(254,226,226,.9)', color: '#991b1b' }
              }
            }
          }
        }
      }
    });
  }

  /* Helpers for the multi-school line datasets */
  function makeDataset(label, data, colour) {
    return {
      label: label, data: data,
      borderColor: colour, backgroundColor: colour,
      tension: 0.3, fill: false,
      pointRadius: 3, pointHoverRadius: 5, borderWidth: 2
    };
  }
  function makeCohortDataset(label, data, colour) {
    return {
      label: label, data: data,
      borderColor: colour, backgroundColor: colour,
      tension: 0.3, fill: false,
      pointRadius: 2, pointHoverRadius: 4, borderWidth: 2,
      borderDash: [6, 4]
    };
  }

});
