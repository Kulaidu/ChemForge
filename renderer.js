document.getElementById('actionButton').addEventListener('click', async () => {
    const response = await fetch('http://localhost:5000/api-endpoint');
    const data = await response.json();
    document.getElementById('result').innerText = JSON.stringify(data);
  });