function splitPngImages(byteArray) {
    // The PNG signature to look for
    const pngSignature = [137, 80, 78, 71];
    const images = [];
    let currentImage = [];
    let index = 0;

    // Iterate through the byteArray
    while (index < byteArray.length) {
        // Check for the PNG signature
        if (byteArray.slice(index, index + pngSignature.length).join(',') === pngSignature.join(',')) {
            // If a new image starts and there's already data in currentImage, push it to images
            if (currentImage.length > 0) {
                images.push(new Uint8Array(currentImage));
            }
            // Start a new image
            currentImage = [];
        }
        // Add the current byte to the current image
        currentImage.push(byteArray[index]);
        index++;
    }

    // Push the last image if there's any
    if (currentImage.length > 0) {
        images.push(new Uint8Array(currentImage));
    }

    return images;
}

async function fetchBinaryFile() {
    try {
        const response = await fetch('assets/decoded_meshgrid.bin');
        if (!response.ok) {
            throw new Error('Failed to fetch binary file');
        }
        const buffer = await response.arrayBuffer();
        const byteArray = new Uint8Array(buffer);

        const splitArray = splitPngImages(byteArray);
        // Remove first element which is not an image
        const pngImages = splitArray.slice(1);

        return pngImages; // List of images

    } catch (error) {
        console.error('Error loading binary file:', error);
        throw error; // rethrow the error to propagate it
    }
}


async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

document.addEventListener('DOMContentLoaded', async function () {
    const cmap = await fetchData('assets/cmap.json');
    fetchBinaryFile().then(images => {

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
            const selectedImageArray = images[pointIndex];

            if (!selectedImageArray || selectedImageArray.length === 0) {
                console.error("Selected image array is undefined or empty.");
                return;
            }

            // Convert as blob
            const blobImage = new Blob([selectedImageArray], { type: 'image/png' });
            const imageUrl = URL.createObjectURL(blobImage);

            // Get selected image html element
            const img = document.getElementById('selected-image');

            // Assign the source of the image
            img.src = imageUrl;
        }

        document.getElementById('plot').on('plotly_click', graphInteraction);
        document.getElementById('plot').on('plotly_hover', graphInteraction);
    });
});
