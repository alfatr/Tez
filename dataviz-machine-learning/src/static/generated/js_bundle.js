$(document).ready(function () {
  // set the dimensions and margins of the graph
  
  //Koşullar sağlanırsa grafiği çizdirmeliyiz.
  var prerequisites = false;
  //Verisetinin URL adresi
  var url = csv_url;
  //Verisetinden seçilen sütunlar
  var arrayOfColumns = columns;

  if(arrayOfColumns.length == 2 && arrayOfColumns[0].Datatype == "Numeric")
  {
    prerequisites = true;
    x_column = arrayOfColumns[1].Column;
    y_column = arrayOfColumns[0].Column;
  }

  if(arrayOfColumns.length == 2 && arrayOfColumns[1].Datatype == "Numeric")
  {
    prerequisites = true;
    x_column = arrayOfColumns[0].Column;
    y_column = arrayOfColumns[1].Column;
  }

  if(prerequisites)
  {
    console.log("Seçilen veri ile barplot oluşturulabiliriz...")
    //Koşullar sağlanırsa DOM içine basic-barplot eklenmeli, direkt sayfa içinde böyle bir alan olmamalı
    $("#graphs").append("<div class='carousel-item'><div id='basic-barplot'></div></div>")
    
    //Eğer grafik çizilecekse açıklama eklemek için...
    // var description = "<b>Basic barplot</b><br>" +
    //   + "<b> Url: </b> " + csv_url + " <br>"
    //   + arrayOfColumns[0].Column + " : " + arrayOfColumns[0].Datatype + "<br>"
    //   + arrayOfColumns[1].Column + " : " + arrayOfColumns[1].Datatype;
                      
    // $("#basic-barplot").parent().append(description)
    var margin = {top: 30, right: 30, bottom: 70, left: 60},
      width = 460 - margin.left - margin.right,
      height = 460 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var barplot_div = d3.select("#basic-barplot")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    d3.csv(url, function(data) 
    {
        // X axis
        var x = d3.scaleBand()
        .range([0, width])
        .domain(data.map(function(d) { return d[x_column]; }))
        .padding(0.2);
        barplot_div.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");
  
        // Add Y axis
        var y = d3.scaleLinear()
        .domain([0, 13000])
        .range([ height, 0]);
        barplot_div.append("g")
        .call(d3.axisLeft(y));
  
        // Bars
        barplot_div.selectAll("mybar")
        .data(data)
        .enter()
        .append("rect")
            .attr("x", function(d) { return x(d[x_column]); })
            .attr("y", function(d) { return y(d[y_column]); })
            .attr("width", x.bandwidth())
            .attr("height", function(d) { return height - y(d[y_column]); })
            .attr("fill", "#69b3a2")
    })
  }
})
$(document).ready(function (){
    //Koşullar sağlanırsa grafiği çizdirmeliyiz.
    var prerequisites = false;
    //Verisetinin URL adresi
    var url = csv_url;
    //Verisetinden seçilen sütunlar
    var arrayOfColumns = columns;

    if(arrayOfColumns.length == 1
        && arrayOfColumns[0].Datatype == "Numeric"
    )
    {
        prerequisites = true;
        y_column = arrayOfColumns[0].Column;
    }
    
    if(prerequisites)
    {
        console.log("Seçilen veri ile histogram oluşturulabiliriz...")
        //Koşullar sağlanırsa DOM içine basic-barplot eklenmeli, direkt sayfa içinde böyle bir alan olmamalı
        $("#graphs").append("<div class='carousel-item'><div id='basic-histogram'></div></div>")
        // var description = "<b>Basic histogram</b><br>" +
        // + "<b> Url: </b> " + csv_url + " <br>"
        // + arrayOfColumns[0].Column + " : " + arrayOfColumns[0].Datatype + "<br>"
                        
        // $("#basic-histogram").parent().append(description)


        var margin = {top: 10, right: 30, bottom: 30, left: 40},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

        // append the svg object to the body of the page
        var histogram_div = d3.select("#basic-histogram")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // get the data
        d3.csv(url, function(data) 
        {

            // X axis: scale and draw:
            var x = d3.scaleLinear()
                .domain([0, 1000])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
                .range([0, width]);
            histogram_div.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // set the parameters for the histogram
            var histogram = d3.histogram()
                .value(function(d) { return d.price; })   // I need to give the vector of value
                .domain(x.domain())  // then the domain of the graphic
                .thresholds(x.ticks(70)); // then the numbers of bins

            // And apply this function to data to get the bins
            var bins = histogram(data);

            // Y axis: scale and draw:
            var y = d3.scaleLinear()
                .range([height, 0]);
                y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            histogram_div.append("g")
                .call(d3.axisLeft(y));

            // append the bar rectangles to the histogram_div element
            histogram_div.selectAll("rect")
                .data(bins)
                .enter()
                .append("rect")
                    .attr("x", 1)
                    .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                    .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
                    .attr("height", function(d) { return height - y(d.length); })
                    .style("fill", "#69b3a2")

            // d3.select("#basic-histogram").attr("align","center");
        });


    }
})
$(document).ready(function (){
  //Koşullar sağlanırsa grafiği çizdirmeliyiz.
  var prerequisites = false;
  //Verisetinin URL adresi
  var url = csv_url;
  //Verisetinden seçilen sütunlar
  var arrayOfColumns = columns;

  if(arrayOfColumns.length == 2 
    && arrayOfColumns[0].Datatype == "Numeric"
    && arrayOfColumns[1].Datatype == "date")
  {
    prerequisites = true;
    y_column = arrayOfColumns[0].Column;
  }

  if(arrayOfColumns.length == 2 
    && arrayOfColumns[1].Datatype == "Numeric"
    && arrayOfColumns[0].Datatype == "date")
  {
    prerequisites = true;
    x_column = arrayOfColumns[0].Column;
    y_column = arrayOfColumns[1].Column;
  }

  // x_column = "date";
  // y_column = "value";

  if(prerequisites)
  {
    console.log("Seçilen veri ile line graph oluşturulabiliriz...")
    //Koşullar sağlanırsa DOM içine basic-barplot eklenmeli, direkt sayfa içinde böyle bir alan olmamalı
    $("#graphs").append("<div class='carousel-item'><div id='basic-line'></div></div>")
    var description = "<b>Basic line</b><br>" +
      + "<b> Url: </b> " + csv_url + " <br>"
      + arrayOfColumns[0].Column + " : " + arrayOfColumns[0].Datatype + "<br>"
      + arrayOfColumns[1].Column + " : " + arrayOfColumns[1].Datatype;
                      
    $("#basic-scatter").parent().append(description)
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;



    // append the svg object to the body of the page
    var line_div = d3.select("#basic-line")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv(csv_url,
    // When reading the csv, I must format variables:
    function(d){
    return { date : d3.timeParse("%Y-%m-%d")(d[x_column]), value : d[y_column] }
    },

    // Now I can use this dataset:
    function(data) {

    // Add X axis --> it is a date format
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d[x_column]; }))
      .range([0, width ]);
    line_div.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return + d[x_column]; })])
      .range([ height, 0 ]);
    line_div.append("g")
      .call(d3.axisLeft(y));

    // Add the line
    line_div.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d[x_column]) })
        .y(function(d) { return y(d[y_column]) })
        )

    })
  }
})
$(document).ready(function (){
  //Koşullar sağlanırsa grafiği çizdirmeliyiz.
  var prerequisites = false;
  //Verisetinin URL adresi
  var url = csv_url;
  //Verisetinden seçilen sütunlar
  var arrayOfColumns = columns;

  if(arrayOfColumns.length == 2 
    && arrayOfColumns[0].Datatype == "Numeric"
    && arrayOfColumns[1].Datatype == "Numeric")
  {
    prerequisites = true;
    x_column = arrayOfColumns[1].Column;
    y_column = arrayOfColumns[0].Column;
  }

  if(prerequisites)
  {
    console.log("Seçilen veri ile scatter oluşturulabiliriz...")
    //Koşullar sağlanırsa DOM içine basic-barplot eklenmeli, direkt sayfa içinde böyle bir alan olmamalı
    $("#graphs").append("<div class='carousel-item'><div id='basic-scatter'></div></div>")
    //Eğer grafik çizilecekse açıklama eklemek için...
    var description = "<b>Basic scatter</b><br>" +
      + "<b> Url: </b> " + csv_url + " <br>"
      + arrayOfColumns[0].Column + " : " + arrayOfColumns[0].Datatype + "<br>"
      + arrayOfColumns[1].Column + " : " + arrayOfColumns[1].Datatype;
                      
    $("#basic-scatter").parent().append(description)
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var scatter_div = d3.select("#basic-scatter")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv(csv_url, function(data) {
      console.log(data)
    // Add X axis
    var x = d3.scaleLinear()
    .domain([0, 4000])
    .range([ 0, width ]);
    scatter_div.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
    .domain([0, 500000])
    .range([ height, 0]);
    scatter_div.append("g")
    .call(d3.axisLeft(y));

    // Add dots
    scatter_div.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
        .attr("cx", function (d) { return x(d[y_column]); } )
        .attr("cy", function (d) { return y(d[x_column]); } )
        .attr("r", 1.5)
        .style("fill", "#69b3a2")

    })
  }
})