$(document).ready(function () {

    console.log(dataset)

    dataset = "/static/datasets/" + dataset

    scores.sort(sortFunction)
    for (i = 0; i < scores.length; i++) {
        console.log(scores[i][0] + " - " + scores[i][1])
        if (scores[i][0] == "Box Plot") {
            BoxPlot_OneNumeric_OneCategorical(i)
        }
        if (scores[i][0] == "Violin") {
            Violin_OneNumeric_OneCategorical(i)
        }
        if (scores[i][0] == "Line") {
            Line_Two_Numerical(i)
        }
    }
})

function sortFunction(a, b) {
    if (a[1] === b[1]) {
        return 0;
    }
    else {
        return (a[1] > b[1]) ? -1 : 1;
    }
}

function BoxPlot_OneNumeric_OneCategorical(index) {
    carousel_item_active = '"'
    classText = ''

    if (index == 0) {
        carousel_item_active = 'active"'
        classText = 'class = "active" '
    }

    var graph = '<div id="boxplot' + index + '" class="carousel-item ' + carousel_item_active + ' style="text-align: center">'
    var indicator = '<li data-target="#carouselExampleIndicators" data-slide-to="' + index + '" ' + classText + '></li>'
    $("#graph-indicators").append(indicator)
    $("#graphs").append(graph)

    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#boxplot" + index)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // create dummy data
    d3.csv(dataset, function (data) {

        min_value = d3.min(data, d => d[numeric_columns[0]])
        max_value = d3.max(data, d => d[numeric_columns[0]])

        min_value = min_value - ((max_value - min_value) / 4)
        max_value = parseFloat(max_value) + parseFloat((max_value - min_value) / 4)


        var group_names = d3.nest()
            .key(function (d) { return d[categorical_columns[0]]; })
            .rollup(function (v) { return v.length; })
            .entries(data);
        groups = []

        group_names.forEach((item) => groups.push(item.key))
        // Compute quartiles, median, inter quantile range min and max --> these info are then used to draw the box.
        var sumstat = d3.nest() // nest function allows to group the calculation per level of a factor
            .key(function (d) { return d[categorical_columns[0]]; })
            .rollup(function (d) {
                q1 = d3.quantile(d.map(function (g) {
                    return g[numeric_columns[0]];
                }).sort(d3.ascending), .25)

                median = d3.quantile(d.map(function (g) {
                    return g[numeric_columns[0]];
                }).sort(d3.ascending), .5)

                q3 = d3.quantile(d.map(function (g) {
                    return g[numeric_columns[0]];
                }).sort(d3.ascending), .75)

                interQuantileRange = q3 - q1
                min = q1 - 1.5 * interQuantileRange
                max = q3 + 1.5 * interQuantileRange
                return ({ q1: q1, median: median, q3: q3, interQuantileRange: interQuantileRange, min: min, max: max })
            })
            .entries(data)

        // Show the X scale
        var x = d3.scaleBand()
            .range([0, width])
            .domain(groups)
            .paddingInner(1)
            .paddingOuter(.5)
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))

        // Show the Y scale
        var y = d3.scaleLinear()
            .domain([min_value, max_value])
            .range([height, 0])
        svg.append("g").call(d3.axisLeft(y))

        // Show the main vertical line
        svg
            .selectAll("vertLines")
            .data(sumstat)
            .enter()
            .append("line")
            .attr("x1", function (d) { return (x(d.key)) })
            .attr("x2", function (d) { return (x(d.key)) })
            .attr("y1", function (d) { return (y(d.value.min)) })
            .attr("y2", function (d) { return (y(d.value.max)) })
            .attr("stroke", "black")
            .style("width", 40)

        // rectangle for the main box
        var boxWidth = 100
        svg
            .selectAll("boxes")
            .data(sumstat)
            .enter()
            .append("rect")
            .attr("x", function (d) { return (x(d.key) - boxWidth / 2) })
            .attr("y", function (d) { return (y(d.value.q3)) })
            .attr("height", function (d) { return (y(d.value.q1) - y(d.value.q3)) })
            .attr("width", boxWidth)
            .attr("stroke", "black")
            .style("fill", "#69b3a2")

        // Show the median
        svg
            .selectAll("medianLines")
            .data(sumstat)
            .enter()
            .append("line")
            .attr("x1", function (d) { return (x(d.key) - boxWidth / 2) })
            .attr("x2", function (d) { return (x(d.key) + boxWidth / 2) })
            .attr("y1", function (d) { return (y(d.value.median)) })
            .attr("y2", function (d) { return (y(d.value.median)) })
            .attr("stroke", "black")
            .style("width", 80)
    })


}

function Violin_OneNumeric_OneCategorical(index) {
    carousel_item_active = '"'
    classText = ''


    if (index == 0) {
        carousel_item_active = 'active"'
        classText = 'class = "active" '
    }

    var graph = '<div id="violin' + index + '" class="carousel-item ' + carousel_item_active + ' style="text-align: center">'
    var indicator = '<li data-target="#carouselExampleIndicators" data-slide-to="' + index + '" ' + classText + '></li>'
    $("#graph-indicators").append(indicator)
    $("#graphs").append(graph)


    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 40 },
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#violin" + index)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Read the data and compute summary statistics for each specie
    d3.csv(dataset, function (data) {

        min_value = d3.min(data, d => d[numeric_columns[0]])
        max_value = d3.max(data, d => d[numeric_columns[0]])

        min_value = min_value - ((max_value - min_value) / 4)
        max_value = parseFloat(max_value) + parseFloat((max_value - min_value) / 4)

        // Build and Show the Y scale
        var y = d3.scaleLinear()
            .domain([min_value, max_value])          // Note that here the Y scale is set manually
            .range([height, 0])
        svg.append("g").call(d3.axisLeft(y))

        var group_names = d3.nest()
            .key(function (d) { return d[categorical_columns[0]]; })
            .rollup(function (v) { return v.length; })
            .entries(data);
        groups = []

        group_names.forEach((item) => groups.push(item.key))
        // Build and Show the X scale. It is a band scale like for a boxplot: each group has an dedicated RANGE on the axis. This range has a length of x.bandwidth
        var x = d3.scaleBand()
            .range([0, width])
            .domain(groups)
            .padding(0.05)     // This is important: it is the space between 2 groups. 0 means no padding. 1 is the maximum.
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))

        // Features of the histogram
        var histogram = d3.histogram()
            .domain(y.domain())
            .thresholds(y.ticks(20))    // Important: how many bins approx are going to be made? It is the 'resolution' of the violin plot
            .value(d => d)

        // Compute the binning for each group of the dataset
        var sumstat = d3.nest()  // nest function allows to group the calculation per level of a factor
            .key(function (d) { return d[categorical_columns[0]]; })
            .rollup(function (d) {   // For each key..
                input = d.map(function (g) { return g[numeric_columns[0]]; })    // Keep the variable called Sepal_Length
                bins = histogram(input)   // And compute the binning on it.
                return (bins)
            })
            .entries(data)

        // What is the biggest number of value in a bin? We need it cause this value will have a width of 100% of the bandwidth.
        var maxNum = 0
        for (i in sumstat) {
            allBins = sumstat[i].value
            lengths = allBins.map(function (a) { return a.length; })
            longuest = d3.max(lengths)
            if (longuest > maxNum) { maxNum = longuest }
        }

        // The maximum width of a violin must be x.bandwidth = the width dedicated to a group
        var xNum = d3.scaleLinear()
            .range([0, x.bandwidth()])
            .domain([-maxNum, maxNum])

        // Add the shape to this svg!
        svg
            .selectAll("myViolin")
            .data(sumstat)
            .enter()        // So now we are working group per group
            .append("g")
            .attr("transform", function (d) { return ("translate(" + x(d.key) + " ,0)") }) // Translation on the right to be at the group position
            .append("path")
            .datum(function (d) { return (d.value) })     // So now we are working bin per bin
            .style("stroke", "none")
            .style("fill", "#69b3a2")
            .attr("d", d3.area()
                .x0(function (d) { return (xNum(-d.length)) })
                .x1(function (d) { return (xNum(d.length)) })
                .y(function (d) { return (y(d.x0)) })
                .curve(d3.curveCatmullRom)    // This makes the line smoother to give the violin appearance. Try d3.curveStep to see the difference
            )
    })

}

function Line_Two_Numerical()
{
    console.log("Line plotting with two numerical variables...")

}