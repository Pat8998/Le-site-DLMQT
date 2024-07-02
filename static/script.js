const jsonFile = '../database/database.json';
let sortedBy = 0;
let sortWay = true;
const ws = new WebSocket('ws://127.0.0.1:20079/ws');

// Function to fetch JSON data from file using fetch API
async function fetchJSONFile(path) {
    return fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });
}

// Function to generate table rows from JSON data
function generateTable(jsonData) {
    const tableBody = document.querySelector("#jsonTable tbody");

        // Clear existing table rows
        while (tableBody.firstChild) {
            tableBody.removeChild(tableBody.firstChild);
        }
    

    jsonData.forEach(rowData => {
        const row = document.createElement("tr");

       // Iterate through keys in rowData
       Object.keys(rowData).forEach((key, index) => {
        const cell = document.createElement("td");
        if (index === 1) { // Check if it's the second column (index 1)
            // Create a button for the second column
            const button = document.createElement("button");
            button.textContent = rowData[key];
            button.addEventListener("click", () => {
                // Define action when button is clicked
                alert(`You clicked row with data: ${JSON.stringify(rowData)}`);
                ws.send('caca')
                // Example: You can perform other actions here based on rowData
            });
            cell.appendChild(button); // Append button to the cell
        } else {
            cell.textContent = rowData[key]; // Otherwise, set text content
        }
        row.appendChild(cell); // Append cell to the row
    });

        tableBody.appendChild(row);
    });
    sortTable(sortedBy, sortWay);
}



// Function to sort table based on clicked header
function sortTable(columnIndex, sortReverse=1) {
    const table = document.getElementById("jsonTable");
    const rows = Array.from(table.querySelectorAll("tbody tr"));

    // Sort rows based on content of the specified column
        rows.sort((rowA, rowB) => {
            const cellA = rowA.querySelectorAll("td")[columnIndex].textContent.trim();
            const cellB = rowB.querySelectorAll("td")[columnIndex].textContent.trim();

            // Adjust comparison based on data type (e.g., numeric vs. string)
            return cellA.localeCompare(cellB, undefined, { numeric: true })*(sortReverse*2-1);
    });

    // Clear existing table rows
    const tbody = table.querySelector("tbody");
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    // Append sorted rows to table
    rows.forEach(row => {
        tbody.appendChild(row);
    });
    table.querySelectorAll("thead tr")[0].querySelectorAll("th").forEach(element => {
        element.textContent = element.textContent.replace(/\u21A7/g, '')
        element.textContent = element.textContent.replace(/\u21A5/g, '')
    });
    const header = table.querySelectorAll("thead tr")[0].querySelectorAll("th")[columnIndex];
    header.textContent =  sortReverse ? "\u21A7"+ header.textContent : "\u21A5"+header.textContent;
    sortedBy=columnIndex;
}
// Example: Attach click event listeners to headers for sorting
document.getElementById("Header name").addEventListener("click", () => {sortWay = !sortWay; sortTable(0, sortWay)}); 
document.getElementById("Header Connected").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(1, sortWay)}); 
document.getElementById("Header MAC").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(2, sortWay)}); 
document.getElementById("Header IP").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(3, sortWay)}); 
document.getElementById("Header LIP").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(4, sortWay)}); 


       // Function to fetch JSON data, generate table, and refresh every 5 seconds
async function fetchDataAndRefresh() {
        // Call fetchJSONFile to load data from database/database.json
    fetchJSONFile(jsonFile)
    .then(data => {
        generateTable(data);
    });
    //setTimeout(fetchDataAndRefresh, 500); // Refresh every .5 seconds
}

ws.onmessage = function (event) {
    console.log('Message from server:', event.data);
    
    fetchDataAndRefresh();
};

ws.onopen = function(event) {
    console.log("Connection established.");
};
fetchDataAndRefresh();
