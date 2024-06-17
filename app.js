async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

document.addEventListener('DOMContentLoaded', async function () {
    const decodedMeshgrid = await fetchData('assets/decoded_meshgrid.json');
    const cmap = await fetchData('assets/cmap.json');
    const gridSize = 100;

    // Define a set of visually distinct colors for the colormap
    const distinctColors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ];

    // Create a function to map values to distinct colors
    function getColor(value) {
        const index = value % distinctColors.length;
        return distinctColors[index];
    }

    // Generate legend dynamically
    const legendContainer = document.getElementById('legend');

    // Labels
    const classLabels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

    // Create legend items
    distinctColors.forEach((color, index) => {
        const li = document.createElement('li');
        li.classList.add('legend-li');
        li.innerHTML = `
            <span class="legend-color" style="background-color: ${color};"></span>
            <span class="legend-text">${classLabels[index]}</span>
        `;
        legendContainer.appendChild(li);
    });

    // Flatten and map the colormap
    const flatCmap = cmap.flat().map(getColor);

    // Create x axis and y axis ticks
    const x_axis = [...Array(gridSize).keys()].map(i => i / (gridSize - 1));
    const y_axis = [...Array(gridSize).keys()].map(i => i / (gridSize - 1));

    // Create coordinates vectors
    const x_coordinates = [];
    const y_coordinates = [];
    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            x_coordinates.push(x_axis[j]);
            y_coordinates.push(y_axis[i]);
        }
    }

    const trace = {
        x: x_coordinates,
        y: y_coordinates,
        mode: 'markers',
        marker: {
            color: flatCmap,
            size: 6, // Increased marker size for better visibility
            opacity: 0.8 // Reduced opacity for smoother appearance
        },
        type: 'scatter',
        hoverinfo: 'none',
    };

    const layout = {
        title: {
            text: `Explore the Latent Space`,
            font: {
                size: 28, // Larger title font size
                family: 'Arial, sans-serif'
            }
        },
        hovermode: 'closest',
        xaxis: {
            scaleanchor: "y",
            scaleratio: 1,
            fixedrange: true,
            title: {
                text: 'First dimension',
                font: {
                    size: 16
                }
            }
        },
        yaxis: {
            scaleanchor: "x",
            scaleratio: 1,
            fixedrange: true,
            title: {
                text: 'Second dimension',
                font: {
                    size: 16
                }
            }
        },
        width: 800, // Increased plot width for better display
        height: 800, // Increased plot height for better display
        margin: { l: 40, r: 40, t: 80, b: 40 }, // Increased margins for better spacing
        plot_bgcolor: '#262626', // Darker plot background
        paper_bgcolor: '#1a1a1a', // Dark background
        font: { color: '#f0f0f0' }, // Light text color
    };

    Plotly.newPlot('plot', [trace], layout);

    function graphInteraction(data) {
        const pointIndex = data.points[0].pointIndex;

        if (pointIndex === undefined) {
            console.error("Invalid point index:", pointIndex);
            return;
        }

        const selectedImageArray = decodedMeshgrid[pointIndex];

        if (!selectedImageArray || selectedImageArray.length === 0) {
            console.error("Selected image array is undefined or empty.");
            return;
        }

        const canvas = document.createElement('canvas');
        const imageShape = [28, 28];
        canvas.width = imageShape[0];
        canvas.height = imageShape[1];
        const ctx = canvas.getContext('2d');
        const imageData = ctx.createImageData(imageShape[0], imageShape[1]);

        for (let i = 0; i < selectedImageArray.length; i++) {
            const value = selectedImageArray[i];
            imageData.data[4 * i] = value;
            imageData.data[4 * i + 1] = value;
            imageData.data[4 * i + 2] = value;
            imageData.data[4 * i + 3] = 255;
        }

        ctx.putImageData(imageData, 0, 0);
        const img = document.getElementById('selected-image');
        img.src = canvas.toDataURL();
    }

    document.getElementById('plot').on('plotly_click', graphInteraction);
    document.getElementById('plot').on('plotly_hover', graphInteraction);
});
