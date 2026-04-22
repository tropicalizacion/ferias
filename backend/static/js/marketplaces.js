// ------------------------------
// Marketplaces by province chart
// ------------------------------

// Data
var nProvinces = document.currentScript.getAttribute('data-n-provinces');
nProvinces = nProvinces.replace('[', '');
nProvinces = nProvinces.replace(']', '');
var nProvinces = nProvinces.split(',').map(Number);

// Configuration
var data = {
    labels: ['San José', 'Alajuela', 'Cartago', 'Heredia', 'Guanacaste', 'Puntarenas', 'Limón'],
    datasets: [{
        label: 'Número de ferias',
        data: nProvinces,
        backgroundColor: ['#EBB615', '#008D4A', '#3879B5', '#D1C5BA', '#E64128', '#CD7535', '#F29196'],
        borderWidth: 0
    }]
};

// Configuration
var config = {
    type: 'bar',
    data: data,
    options: {
        responsive: true,
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
};

// Create the chart
const chartProvinces = new Chart(document.getElementById('n-provinces'), config);

// --------------------------
// Marketplaces by days chart
// --------------------------

// Data
var nDays = document.currentScript.getAttribute('data-n-days');
nDays = nDays.replace('[', '');
nDays = nDays.replace(']', '');
var nDays = nDays.split(',').map(Number);

// Configuration
var data = {
    labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
    datasets: [{
        label: 'Número de ferias',
        data: nDays,
        backgroundColor: ['#EBB615', '#008D4A', '#3879B5', '#D1C5BA', '#E64128', '#CD7535', '#F29196'],
        borderWidth: 0
    }]
};

// Configuration
var config = {
    type: 'bar',
    data: data,
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                grid: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Cantidad de ferias que están abiertas'
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
};

// Create the chart
const chartDays = new Chart(document.getElementById('n-days'), config);

// -------------------------------
// Marketplaces by amenities chart
// -------------------------------

// Data
var nAmenities = document.currentScript.getAttribute('data-n-amenities');
nAmenities = nAmenities.replace('[', '');
nAmenities = nAmenities.replace(']', '');
var nAmenities = nAmenities.split(',').map(Number);

// Configuration
var data = {
    labels: ['Comidas', 'Bebidas', 'Artesanías', 'Carnicería', 'Lácteos', 'Pescadería', 'Plantas', 'Flores'],
    datasets: [{
        label: 'Porcentajes de ferias que ofrecen',
        data: nAmenities,
        backgroundColor: ['#EBB615', '#008D4A', '#3879B5', '#D1C5BA', '#E64128', '#CD7535', '#F29196', '#EBB615'],
        borderWidth: 0
    }]
};

// Configuration
var config = {
    type: 'bar',
    data: data,
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                grid: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Porcentaje de ferias que ofrecen'
                }
            },
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
};

// Create the chart
const chartAmenities = new Chart(document.getElementById('n-amenities'), config);

// ------------------------------------
// Marketplaces by infrastructure chart
// ------------------------------------

// Data
var nInfrastructure = document.currentScript.getAttribute('data-n-infrastructure');
nInfrastructure = nInfrastructure.replace('[', '');
nInfrastructure = nInfrastructure.replace(']', '');
var nInfrastructure = nInfrastructure.split(',').map(Number);

// Configuration
var data = {
    labels: ['Campo ferial', 'Bajo techo', 'Estacionamiento'],
    datasets: [{
        label: 'Porcentajes de ferias que ofrecen',
        data: nInfrastructure,
        backgroundColor: ['#EBB615', '#008D4A', '#3879B5'],
        borderWidth: 0
    }]
};

// Configuration
var config = {
    type: 'bar',
    data: data,
    options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
            x: {
                beginAtZero: true,
                max: 100,
                grid: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Porcentaje de ferias que ofrecen'
                }
            },
            y: {
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
};

// Create the chart
const chartInfrastructure = new Chart(document.getElementById('n-infrastructure'), config);
