barGraphIntstruction = '''
Where data is:
{
  labels: string[],
  values: { data: number[], label: string }[]
}

// Usage notes:
- Each label corresponds to an x-axis column.
- Each object in values represents a different series/entity.

// Examples:
1. Average income per month:
data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  values: [{ data: [21.5, 25.0, 47.5, 64.8, 105.5, 133.2], label: 'Income' }]
}

2. American vs European players:
data = {
  labels: ['Series A', 'Series B', 'Series C'],
  values: [
    { data: [10, 15, 20], label: 'American' },
    { data: [20, 25, 30], label: 'European' }
  ]
}
'''


horizontalBarGraphIntstruction = '''
Where data is:
{
  labels: string[],
  values: { data: number[], label: string }[]
}

// Usage notes:
- Same as Bar Graph, but bars are horizontal.

// Examples:
1. Average income per month:
data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  values: [{ data: [21.5, 25.0, 47.5, 64.8, 105.5, 133.2], label: 'Income' }]
}

2. American vs European players:
data = {
  labels: ['Series A', 'Series B', 'Series C'],
  values: [
    { data: [10, 15, 20], label: 'American' },
    { data: [20, 25, 30], label: 'European' }
  ]
}
'''


lineGraphIntstruction = '''
Where data is:
{
  xValues: number[] | string[],
  yValues: { data: number[], label?: string }[]
}

// Usage notes:
- Each xValue corresponds to a point on the x-axis.
- Each object in yValues is one line series.

// Examples:
1. Momentum vs year:
data = {
  xValues: ['2020', '2021', '2022', '2023', '2024'],
  yValues: [{ data: [2, 5.5, 2, 8.5, 1.5] }]
}

2. American vs European players:
data = {
  xValues: ['2020', '2021', '2022', '2023', '2024'],
  yValues: [
    { data: [2, 5.5, 2, 8.5, 1.5], label: 'American' },
    { data: [3, 6, 4, 9, 2], label: 'European' }
  ]
}
'''


pieChartIntstruction = '''
Where data is:
{
  id: number,
  value: number,
  label: string
}[]

// Usage notes:
- Each object represents one slice of the pie.

// Example:
data = [
  { id: 0, value: 10, label: 'Series A' },
  { id: 1, value: 15, label: 'Series B' },
  { id: 2, value: 20, label: 'Series C' }
]
'''


scatterPlotIntstruction = '''
Where data is:
{
  series: {
    data: { x: number, y: number, id: number }[],
    label: string
  }[]
}

// Usage notes:
- Each object in series = one group of points.
- Each point is defined by { x, y, id }.

// Examples:
1. Men vs Women (spending vs quantity):
data = {
  series: [
    {
      data: [
        { x: 100, y: 200, id: 1 },
        { x: 120, y: 100, id: 2 },
        { x: 170, y: 300, id: 3 }
      ],
      label: 'Men'
    },
    {
      data: [
        { x: 300, y: 300, id: 1 },
        { x: 400, y: 500, id: 2 },
        { x: 200, y: 700, id: 3 }
      ],
      label: 'Women'
    }
  ]
}

2. Players (height vs weight):
data = {
  series: [
    {
      data: [
        { x: 180, y: 80, id: 1 },
        { x: 170, y: 70, id: 2 },
        { x: 160, y: 60, id: 3 }
      ],
      label: 'Players'
    }
  ]
}
'''

graph_type_instructions = {
    "bar": barGraphIntstruction,
    "horizontal_bar": horizontalBarGraphIntstruction,
    "line": lineGraphIntstruction,
    "pie": pieChartIntstruction,
    "scatter": scatterPlotIntstruction
}