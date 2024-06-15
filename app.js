async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

document.addEventListener('DOMContentLoaded', async function () {
    const decodedMeshgrid = await fetchData('assets/decoded_meshgrid.json');
    const cmap = await fetchData('assets/cmap.json');
    const gridSize = 100;

    // Define Seaborn-like "tab10" colormap
    const tab10Colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ];

    // Create a function to map values to colors
    function getColor(value) {
        const index = value;
        return tab10Colors[index];
    }

    // Generate legend dynamically
    const legendContainer = document.getElementById('legend');

    // Labels
    const classLabels = ["0", "1", "2", "3", "4",
        "5", "6", "7", "8", "9"];

    // Create legend items
    tab10Colors.forEach((color, index) => {
        const li = document.createElement('li');
        li.style.listStyle = 'none'; // Remove default list style
        li.style.marginBottom = '5px'; // Adjust spacing between legend items
        li.innerHTML = `
            <span class="legend-color" style="background-color: ${color};"></span>
            <span class="legend-text">${classLabels[index]}</span>
        `;
        legendContainer.appendChild(li);
    });

    // Flatten and map the colormap
    const flatCmap = cmap.flat().map(getColor);

    // Create x axis and y axis ticks prior to create coordinates vectors of size 10_000 
    const x_axis = [...Array(gridSize).keys()].map(i => i / (gridSize - 1));
    const y_axis = [...Array(gridSize).keys()].map(i => i / (gridSize - 1));

    // Create coordinates vectors used to map the plot
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
            size: 5
        },
        type: 'scatter',
        hoverinfo: 'none',
    };

    const layout = {
        title: {
            text: `Autoencoder latent space,<br>areas colored based on corresponding encoded digits`,
            font: {
                size: 18,
                family: 'Arial, sans-serif'
            }
        },
        hovermode: 'closest',
        xaxis: { scaleanchor: "y", scaleratio: 1, fixedrange: true },
        yaxis: { scaleanchor: "x", scaleratio: 1, fixedrange: true },
        width: 550,  // Adjust width for the colormap plot
        height: 550, // Adjust height for the colormap plot
        margin: { l: 20, r: 20, t: 60, b: 20 } // Adjust margins as needed
    };

    Plotly.newPlot('plot', [trace], layout);

    function graphInteraction(data) {
        const pointIndex = data.points[0].pointIndex;

        // Check if pointIndex is valid
        if (pointIndex === undefined) {
            console.error("Invalid point index:", pointIndex);
            return;
        }

        // Retrieve the selected image array
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

        // Fill imageData with selectedImageArray
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
