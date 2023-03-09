c = 0.551915024494
radians = (theta) => theta * Math.PI / 180
map = (value, min) => value * (285 - 35) / 100 - 35
degrees = (radians) => radians * (180/ Math.PI)
if (confidence > 1) {
  confidence = 1;
}
if (confidence < .5) {
    SCORE = 50
} else {
    if (result == 0) {
        // 0 < score < 30
        SCORE = 15
        SCORE -= (confidence - 0.75) * 60
    } else {
        // 70 < score < 100
        SCORE = 85
        SCORE += (confidence - 0.75) * 60
    }
    
}

function drawBezierSemicircle(x0,y0,x1,y1) {
    // Find the distance between the points (hypotenuse)
    let d = Math.hypot((x0-x1),(y0-y1))
    // Scale the control handle radius by multiplying the diameter by `c`
    let r = d/2 * c
    // The midpoint of the baseline
    let mid = [(x0+x1)/2,(y0+y1)/2]
    // Returns positive 1 if up, and -1 if down
    let direction = ((x0 < x1) ? 1 : -1);
    // Calculate the overall rotation of the circle
    let rot = degrees(Math.atan((y1-mid[1])/(x1-mid[0])));
    // The parallel angle to the rotation
    let rotParallel = radians((direction * 90) + rot);
    // The apex of the semicircle
    let apex = [Math.cos(rotParallel)*(d/2)+mid[0],Math.sin(rotParallel)*(d/2)+mid[1]]
    
    // Each anchor point needed to draw two bezier curves that make up the semicircle
    let p0 = [x0+Math.cos(rotParallel)*r,y0+Math.sin(rotParallel)*r];
    let p1 = [apex[0]-Math.cos(radians(rot))*r*direction,apex[1]-Math.sin(radians(rot))*r*direction]
    let p2 = [apex[0]+Math.cos(radians(rot))*r*direction,apex[1]+Math.sin(radians(rot))*r*direction]
    let p3 = [x1+Math.cos(rotParallel)*r,y1+Math.sin(rotParallel)*r];
    return ({
      structs: `
        M ${x0},${y0}
        L ${x1},${y1}
        M ${mid[0]},${mid[1]}
        L ${apex[0]} ${apex[1]}
      `,
      handles: `
        M ${x0},${y0}
        L ${p0[0]},${p0[1]}
        M ${apex[0]},${apex[1]}
        L ${p1[0]} ${p1[1]} 
        M ${apex[0]},${apex[1]}
        L ${p2[0]} ${p2[1]}
        M ${x1},${y1}
        L ${p3[0]} ${p3[1]}
      `,
      path: `
        M ${x0},${y0}
        C ${p0[0]},${p0[1]}
          ${p1[0]},${p1[1]}
          ${apex[0]} ${apex[1]}
        C ${p2[0]} ${p2[1]}
          ${p3[0]} ${p3[1]}
          ${x1} ${y1}
      `
    });
}

var gaugeDiv = document.getElementById("gauge-chart");

var wheel = {
  "type": "pie",
  "showlegend": false,
  "hole": 0.75,
  "rotation": 225,
  "values": [3,3,3,3],
  "text": ["True", "Uncertain", "False", ""],
  "direction": "clockwise",
  "textinfo": "text",
  "textposition": "inside",
  "marker": {
    "colors": ["rgba(144, 238, 144, 0.6)", "rgba(165, 165, 165, 0.6)", "rgba(255, 0, 0, 0.6)", "#222831"],
    "line": {
        "width": 4,
        "color": "#222831",
    }
  },
  "hoverinfo": "none",
};

pointer = ({
    type: 'path',
    path: function() {
        const radius = 0.45;
        const size = 0.025;

        let theta = map(SCORE);
        let rads = radians(theta);
        let x1 = -1 * radius * Math.cos(rads) + 0.5;
        let y1 = radius * Math.sin(rads) + 0.5;
        let p0 = [-1 * size * Math.cos(radians(theta-90)) + 0.5,
                    size * Math.sin(radians(theta-90)) + 0.5]
        let p1 = [-1 * size * Math.cos(radians(theta+90)) + 0.5,
                    size * Math.sin(radians(theta+90)) + 0.5]
                return `
            M ${x1} ${y1}
            L ${p0[0]} ${p0[1]}
            L ${p1[0]} ${p1[1]}
    ${drawBezierSemicircle(p1[0],p1[1],p0[0],p0[1]).path}
            Z`;
    }(),
    fillcolor: "#EEEEEE",
    line: {
        width: 0
    }
})

score_value = ({
    "title": "CONFIDENCE",
    "type": "indicator",
    "mode": "number",
    "number": {"suffix": "%", "valueformat": ".0f"},
    "value": confidence * 100,
    "domain": {"x": [0], "y": [0.02, 0.30]}
  })

var options = {
    staticPlot: true,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    showlegend: false,
    displayModeBar: false,
    margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 40,
        pad: 0
    },
    shapes: [pointer],
    width: 500,
    height: 500,
}

Plotly.newPlot(gaugeDiv, [score_value, wheel], options);
