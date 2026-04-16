/* ===================================================
   Melbourne Metrics — Prototype Sketches
   Main JavaScript file.
   Handles assessor role tabs and Chart.js dashboard
   charts for Sketch 5 (multi-school comparison).
   =================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* -------------------------------------------------
     1. Assessor role tabs (Sketch 2)
     ------------------------------------------------- */
  var assessorTabs = document.querySelectorAll('.assessor-tab');
  var assessorSelect = document.getElementById('assessorRoleSelect');

  assessorTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      assessorTabs.forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      // Keep the dropdown in the form header in sync
      if (assessorSelect) {
        assessorSelect.value = tab.dataset.role;
      }
    });
  });

  /* -------------------------------------------------
     2. Chart.js — Wellbeing & Sustainability Dashboard
     Multi-school comparison with realistic noisy data.
     ------------------------------------------------- */
  initDashboardCharts();

  function initDashboardCharts() {

    // Shared chart defaults
    Chart.defaults.font.family = "'Open Sans', Arial, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#52525b';

    /* ---------------------------------------------
       Sample data for four schools + cohort average.
       Terms are spaced at standard IB collection
       points. Data includes realistic noise and
       seasonal patterns (dips in holiday terms,
       peaks around moderation windows).
       --------------------------------------------- */
    var terms = ['T1 2025', 'T2 2025', 'T3 2025', 'T4 2025', 'T1 2026', 'T2 2026'];

    // School colour assignments — neutral, legible
    var colours = {
      greenfield: '#1d4ed8',     // steady blue
      riverside:  '#059669',     // teal-green (recovery school)
      summit:     '#dc2626',     // red (at-risk)
      horizon:    '#7c3aed',     // purple
      cohort:     '#64748b'      // grey, dashed
    };

    /* --- Panel: Activity volume (Ruby telemetry) ---
       Evidence items uploaded per teacher per month.
       Reflects a term-by-term picture with noise. */
    var activityGreenfield = [4.2, 5.1, 6.3, 5.8, 5.4, 6.0];
    var activityRiverside  = [2.8, 5.2, 8.1, 9.8, 8.4, 7.6];
    var activitySummit     = [6.4, 8.2, 11.5, 13.8, 15.2, 16.4];
    var activityHorizon    = [3.6, 4.2, 5.8, 6.4, 6.1, 6.5];
    var activityCohort     = [4.3, 5.7, 7.9, 8.9, 8.8, 9.1];

    new Chart(document.getElementById('chartActivity'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', activityGreenfield, colours.greenfield),
          makeDataset('Riverside Academy',        activityRiverside,  colours.riverside),
          makeDataset('Summit International',     activitySummit,     colours.summit),
          makeDataset('Horizon College',          activityHorizon,    colours.horizon),
          makeCohortDataset('Cohort average',     activityCohort,     colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: {
            min: 0,
            max: 20,
            title: { display: true, text: 'Evidence items per teacher per month' }
          }
        }
      }
    });

    /* --- Panel: Perceived time investment (survey) ---
       Likert 1 (none) to 5 (very heavy). Termly.      */
    var timeGreenfield = [2.3, 2.5, 2.6, 2.4, 2.5, 2.6];
    var timeRiverside  = [2.8, 3.4, 4.0, 3.8, 3.6, 3.5];
    var timeSummit     = [3.2, 3.8, 4.1, 4.3, 4.5, 4.6];
    var timeHorizon    = [2.4, 2.7, 2.9, 3.0, 2.9, 3.0];
    var timeCohort     = [2.7, 3.1, 3.4, 3.4, 3.4, 3.4];

    new Chart(document.getElementById('chartTime'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', timeGreenfield, colours.greenfield),
          makeDataset('Riverside Academy',        timeRiverside,  colours.riverside),
          makeDataset('Summit International',     timeSummit,     colours.summit),
          makeDataset('Horizon College',          timeHorizon,    colours.horizon),
          makeCohortDataset('Cohort average',     timeCohort,     colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: {
            min: 1, max: 5,
            title: { display: true, text: 'Likert (1 none → 5 very heavy)' }
          }
        }
      }
    });

    /* --- Panel: Perceived workload burden (survey) ---
       Likert 1 (very manageable) to 5 (unsustainable). */
    var burdenGreenfield = [2.1, 2.3, 2.4, 2.3, 2.3, 2.4];
    var burdenRiverside  = [2.5, 2.9, 3.6, 3.8, 3.3, 3.2];  // intervention after T4
    var burdenSummit     = [2.9, 3.4, 3.8, 4.1, 4.3, 4.4];
    var burdenHorizon    = [2.3, 2.5, 2.7, 2.8, 2.7, 2.8];
    var burdenCohort     = [2.5, 2.8, 3.1, 3.3, 3.2, 3.2];

    new Chart(document.getElementById('chartWorkload'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', burdenGreenfield, colours.greenfield),
          makeDataset('Riverside Academy',        burdenRiverside,  colours.riverside),
          makeDataset('Summit International',     burdenSummit,     colours.summit),
          makeDataset('Horizon College',          burdenHorizon,    colours.horizon),
          makeCohortDataset('Cohort average',     burdenCohort,     colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: {
            min: 1, max: 5,
            title: { display: true, text: 'Likert (1 very manageable → 5 unsustainable)' }
          }
        },
        plugins: {
          annotation: {
            annotations: {
              amber: {
                type: 'line', yMin: 3.5, yMax: 3.5,
                borderColor: '#f59e0b', borderWidth: 1.5, borderDash: [5, 4],
                label: { display: true, content: 'Amber threshold (3.5)', position: 'start', font: { size: 10 }, backgroundColor: 'rgba(254,243,199,.9)', color: '#78350f' }
              },
              red: {
                type: 'line', yMin: 4.0, yMax: 4.0,
                borderColor: '#dc2626', borderWidth: 1.5, borderDash: [5, 4],
                label: { display: true, content: 'Red threshold (4.0)', position: 'start', font: { size: 10 }, backgroundColor: 'rgba(254,226,226,.9)', color: '#991b1b' }
              }
            }
          }
        }
      }
    });

    /* --- Panel: WHO-5 Wellbeing Index ---
       Validated 5-item instrument, 0–100. Threshold
       50 indicates need for attention. Termly survey. */
    var wellbeingGreenfield = [72, 70, 71, 73, 72, 71];
    var wellbeingRiverside  = [68, 65, 58, 55, 62, 64];  // dipped then recovered
    var wellbeingSummit     = [66, 62, 56, 50, 47, 45];  // crossed threshold
    var wellbeingHorizon    = [70, 69, 67, 68, 67, 68];
    var wellbeingCohort     = [69, 66, 63, 61, 62, 62];

    new Chart(document.getElementById('chartWellbeing'), {
      type: 'line',
      data: {
        labels: terms,
        datasets: [
          makeDataset('Greenfield International', wellbeingGreenfield, colours.greenfield),
          makeDataset('Riverside Academy',        wellbeingRiverside,  colours.riverside),
          makeDataset('Summit International',     wellbeingSummit,     colours.summit),
          makeDataset('Horizon College',          wellbeingHorizon,    colours.horizon),
          makeCohortDataset('Cohort average',     wellbeingCohort,     colours.cohort)
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: { mode: 'index', intersect: false },
        scales: {
          y: {
            min: 30, max: 100,
            title: { display: true, text: 'WHO-5 Wellbeing Index (0–100)' }
          }
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

  /* -------------------------------------------------
     Helper: build a standard school dataset for the
     line charts. Returns a Chart.js dataset object.
     ------------------------------------------------- */
  function makeDataset(label, data, colour) {
    return {
      label: label,
      data: data,
      borderColor: colour,
      backgroundColor: colour,
      tension: 0.3,
      fill: false,
      pointRadius: 3,
      pointHoverRadius: 5,
      borderWidth: 2
    };
  }

  /* -------------------------------------------------
     Helper: build a dashed cohort-average dataset so
     that the benchmark line stands out from the
     per-school series.
     ------------------------------------------------- */
  function makeCohortDataset(label, data, colour) {
    return {
      label: label,
      data: data,
      borderColor: colour,
      backgroundColor: colour,
      tension: 0.3,
      fill: false,
      pointRadius: 2,
      pointHoverRadius: 4,
      borderWidth: 2,
      borderDash: [6, 4]
    };
  }

});
