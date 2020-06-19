$(document).ready(function(){
    console.log("app.js -> Document ready function")
    domRect = $("#first-graph")[0].getBoundingClientRect();
    console.log(domRect)
    
    data = JSONdata 
    scatterPlot(data)
})

//Oluşturulan grafikler verilen div elemanının genişliğine göre resizable olmalı
//Yoksa işin bir esprisi yok
//Bunun için de parametre olarak append yapılacak elemanın height ve width değerleri okunmalı


function scatterPlot(data){
    // set the dimensions and margins of the graph
    var margin = 
    {
        top: 10, 
        right: 30, 
        bottom: 30, 
        left: 60
    },

    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#first-graph")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    // // Add X axis
    var x = d3.scaleLinear()
    .domain([0, 5])
    .range([ 0, width ]);
    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
    .domain([0, 5])
    .range([ height, 0]);
    svg.append("g")
    .call(d3.axisLeft(y));

    // Add dots
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", function (d) { return x(d['petal.length']); } )
    .attr("cy", function (d) { return y(d['petal.width']); } )
    .attr("r", 1.5)
    .style("fill", "#69b3a2")
}



