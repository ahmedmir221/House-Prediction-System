async function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Convert area_size to a float explicitly
    data.area_size = parseFloat(data.area_size);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        console.log("Response:", response); // Log the response for debugging

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Server error');
        }

        const result = await response.json();
        document.getElementById('result').innerHTML = `<h2>Predicted Price: ${result.price}</h2>`;
    } catch (error) {
        document.getElementById('result').innerHTML = `<h2>Error: ${error.message}</h2>`;
    }
}
