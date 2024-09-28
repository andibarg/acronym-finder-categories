// Run search function when typing
$('#search-input').on('keyup', function(){
  var value = $(this).val()
  console.log('Value:', value)
  var data = searchTable(value, acronymList)
  buildTable(data)
})

// Build initial table
buildTable(acronymList)

// Function to search and filter data
function searchTable(value, data){
  var filteredData = []
  
  // Loop through rows
  for (var i = 0; i < data.length; i++){

    // Make lower case values
    value = value.toLowerCase()
    var acronym = data[i].acronym.toLowerCase()
    var terms = data[i].term.toLowerCase()
		
    // Push if values are matched
    if (acronym.includes(value) | terms.includes(value)){
      filteredData.push(data[i])}
  }
  return filteredData
}

// Function to build data table
function buildTable(data){
  var table = document.getElementById('acronymTable')
  table.innerHTML = ''
	
  // Loop through rows and fill values from data
  for (var i = 0; i < data.length; i++){
    var row = `<tr>
               <td>${data[i].acronym}</td>
               <td>${data[i].term}</td>
               <td>${data[i].category}</td>
                </tr>`
    table.innerHTML += row
  }
}

// Get variable into html
document.getElementById("lastUpdate").textContent = lastUpdate; 