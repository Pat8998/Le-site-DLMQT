const jsonFile = '../database/database.json';
let sortedBy = 0;
let sortWay = true;
let ws = null; // Initialize as null


async function server_ip() {
    const response = await fetch('ip');
    const data = await response.text(); // Assuming the response contains plain text IP address
    return data;
}
function copyToClipboard(text) {
    // Create a textarea element dynamically
    const textarea = document.createElement('textarea');
    
    // Set the value of the textarea to the text to be copied
    textarea.value = text;
    
    // Make the textarea out of view by setting absolute positioning and moving it out of the viewport
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '-9999px';
    
    // Append the textarea to the document body
    document.body.appendChild(textarea);
    
    // Select the text in the textarea
    textarea.select();
    
    // Execute the copy command
    document.execCommand('copy');
    
    // Remove the textarea from the document body
    document.body.removeChild(textarea);
    var statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = 'Copied '+text;
    statusMessage.style.display = 'inline-block'; // Show the status message
    setTimeout(function() {
        statusMessage.style.display = 'none'; // Hide the status message after 3 seconds
    }, 1000); // 3000 milliseconds (3 seconds) for example
}
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
        if (index == 1) { // Check if it's the second column (index 1)
            // Create a button for the second column
            const button = document.createElement("button");
            button.textContent = rowData[key];
            button.addEventListener("click", () => {
                fetch('disconnect?device='+encodeURIComponent(rowData['MAC'])).then(
                    response => response.text().then(value => {
                        if (value == 'Success'){
                            console.log('Successfully disconnected device:'+rowData['name'])
                        } else {
                            
                            alert(`Failed to Disconnect ${rowData['name']} (MAC: ${rowData['MAC']})`);
                        }}))})
            cell.appendChild(button); // Append button to the cell
        } else if(index > 4) { // Check if it's the last 2 rows
            // Create a button for the those
            const button = document.createElement("button");
            button.textContent = rowData[key];
            button.addEventListener("click", () => {
                fetch('change_priority?device=' + encodeURIComponent(rowData['MAC']) + 
      '&priority=' + encodeURIComponent((index - 5) ? "VIP" : "blacklist") + 
      '&previousvalue=' + encodeURIComponent(rowData[key])).then( 
                    response => response.text().then(value => {
                        if (value == 'Success'){
                            console.log('Successfully changed value: '+rowData['name'])
                        } else {
                            
                            alert(`Failed to Change Value ${rowData['name']} (MAC: ${rowData['MAC']})`);
                        }}))})
            cell.appendChild(button); // Append button to the cell
        } else {
            cell.textContent = rowData[key]; // Otherwise, set text content
            cell.addEventListener("click", () =>  {copyToClipboard(cell.textContent)})
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
document.getElementById("Header Blacklist").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(5, sortWay)}); 
document.getElementById("Header VIP").addEventListener("click", () =>  {sortWay = !sortWay; sortTable(6, sortWay)}); 


       // Function to fetch JSON data, generate table, and refresh every 5 seconds
async function fetchDataAndRefresh() {
        // Call fetchJSONFile to load data from database/database.json
    fetchJSONFile(jsonFile)
    .then(data => {
        generateTable(data);
    });
    //setTimeout(fetchDataAndRefresh, 500); // Refresh every .5 seconds
}






function createWebSocket(ip) {
    if (ws) {
        // Close existing WebSocket connection if it's open
        ws.close();
    }

    ws = new WebSocket('ws://' + ip + ':6969/ws');

    ws.onopen = function() {
        console.log("Connection established.");
        
        fetchDataAndRefresh();
        // Additional logic upon WebSocket open
    };

    ws.onmessage = function(event) {
        console.log('Message from server:', event.data);
        
        fetchDataAndRefresh();
    };

    ws.onclose = function(event) {
        console.log('WebSocket connection closed.');
        connectToServer();
        // reConnect when it disconnects
    };

    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
        // Handle WebSocket error
    };

}async function connectToServer() {
    const ip = await server_ip();
    createWebSocket(ip);
}



connectToServer();
fetchDataAndRefresh();