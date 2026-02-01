// Global Sidebar Toggle Function (Must be outside DOMContentLoaded)
function toggleSidebar() {
    const sidebar = document.getElementById("sidebarUI");
    if (sidebar) {
        sidebar.classList.toggle("active");
    } else {
        console.error("Sidebar element not found!");
    }
}

// Chart Instances
let mainChartInstance = null;
let radarChartInstance = null;
let pieChartInstance = null;

document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('predictionForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show Loading
            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            btn.disabled = true;

            // Collect Data
            const formData = {
                weight_capacity: parseFloat(document.getElementById('weight').value),
                category: document.getElementById('category').value,
                fragility_score: parseInt(document.getElementById('fragilityScore').value),
                shelf_life_days: parseInt(document.getElementById('shelfLife').value),
                dimensions: {
                    l: parseFloat(document.getElementById('dimL').value),
                    w: parseFloat(document.getElementById('dimW').value),
                    h: parseFloat(document.getElementById('dimH').value)
                }
            };

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                const data = await response.json();

                if (data.status === 'success') {
                    updateUI(data.recommendations);
                    // Close Sidebar on success for mobile feel
                    toggleSidebar();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to connect to AI server.');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    }
});

function updateUI(results) {
    // Hide Placeholder, Show Results
    document.getElementById('initialState').classList.add('d-none');
    document.getElementById('resultsSection').classList.remove('d-none');

    const top = results[0];

    // Update Top Card
    document.getElementById('topName').innerText = top.material_type;
    document.getElementById('topScore').innerText = top.suitability_score;
    document.getElementById('topCO2').innerText = top.predicted_co2;
    document.getElementById('topCost').innerText = top.predicted_cost_efficiency;

    // Update Table
    const tbody = document.getElementById('rankingTableBody');
    tbody.innerHTML = '';
    results.forEach((item, index) => {
        const row = `
            <tr>
                <td><span class="badge bg-${index === 0 ? 'success' : 'secondary'} rounded-pill">${index + 1}</span></td>
                <td class="fw-bold">${item.material_type}</td>
                <td>
                    <div class="d-flex align-items-center">
                        <span class="me-2">${item.suitability_score}</span>
                        <div class="progress flex-grow-1" style="height: 6px;">
                            <div class="progress-bar bg-success" role="progressbar" style="width: ${item.suitability_score}%"></div>
                        </div>
                    </div>
                </td>
                <td>${item.biodegradability} / 100</td>
                <td>${item.predicted_co2} units</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    // Render Charts
    renderMainChart(results.slice(0, 5));
    renderRadarChart(top);
    renderPieChart(results.slice(0, 5));
}

function renderMainChart(data) {
    const ctx = document.getElementById('mainChart').getContext('2d');
    const labels = data.map(d => d.material_type);
    
    if (mainChartInstance) mainChartInstance.destroy();

    mainChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Cost Efficiency', data: data.map(d => d.predicted_cost_efficiency), backgroundColor: '#10b981', borderRadius: 5, yAxisID: 'y' },
                { label: 'CO₂ Impact', data: data.map(d => d.predicted_co2), backgroundColor: '#3b82f6', borderRadius: 5, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { type: 'linear', display: true, position: 'left', grid: { display: false } },
                y1: { type: 'linear', display: true, position: 'right', grid: { display: false } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function renderRadarChart(item) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Biodegradability', 'Recyclability', 'Tensile Str.', 'Moisture Barrier', 'Cost Eff.'],
            datasets: [{
                label: item.material_type,
                data: [
                    item.biodegradability,
                    item.recyclability,
                    Math.min(100, item.tensile_strength * 1.5), 
                    85, // Dummy visual for Moisture
                    Math.min(100, item.predicted_cost_efficiency * 5)
                ],
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderColor: '#10b981',
                pointBackgroundColor: '#10b981'
            }]
        },
        options: {
            scales: { r: { suggestMin: 0, suggestedMax: 100 } },
            plugins: { legend: { display: false } }
        }
    });
}

function renderPieChart(data) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    if (pieChartInstance) pieChartInstance.destroy();

    pieChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.material_type),
            datasets: [{
                data: data.map(d => d.suitability_score),
                backgroundColor: [
                    '#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { 
                legend: { position: 'bottom', labels: { boxWidth: 10 } } 
            },
            cutout: '70%'
        }
    });
}
