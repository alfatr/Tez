var data = [4, 8, 15, 16, 23, 42]

$(document).ready(function(){
    console.log("Document ready function")

    // Bar Chart Oluştur
    var barElement = createBarChart()
    console.log(barElement)
    $("#barChartContainer").append(barElement)
});

function createBarChart()
{
    // Create an empty (detached) chart container.
    const div = d3.create("div");
    
    // Apply some styles to the chart container.
    div.style("font", "10px sans-serif");
    div.style("text-align", "right");
    div.style("color", "white");
    
    // Define the initial (empty) selection for the bars.
    const bar = div.selectAll("div");
    
    // Bind this selection to the data (computing enter, update and exit).
    const barUpdate = bar.data(data);
    
    // Join the selection and the data, appending the entering bars.
    const barNew = barUpdate.join("div");
    
    // Apply some styles to the bars.
    barNew.style("background", "steelblue");
    barNew.style("padding", "3px");
    barNew.style("margin", "1px");
    
    // Set the width as a function of data.
    barNew.style("width", d => `${d * 10}px`);
    
    // Set the text of each bar as the data.
    barNew.text(d => d);
    
    // Return the chart container.
    return div.node();
}