var listeners_set = false;
new MutationObserver(function(m) {
    if (!listeners_set) {
        n_graphs = 3;
        for (var i=0; i < n_graphs; i++) {
            var element = document.getElementById("graph" + i);
            if (element) {
                element.on("plotly_selected", function(event_data) {
                    var selected_data = []
                    for (var j=0; j < event_data.points.length; j++) {
                        selected_data.push(event_data.points[j].text);
                    }
                    for (var k=0; k < n_graphs; k++) {
                        var element2 = document.getElementById("graph" + k);
                        if (element2) {
                            var opacities = [];
                            for (var l=0; l < element2.data[0].text.length; l++) {
                                if (selected_data.indexOf(element2.data[0].text[l]) > -1) {
                                    opacities.push(1.0);
                                } else {
                                    opacities.push(0.2);
                                }
                            }
                            Plotly.restyle(element2, {
                                selectedpoints: [null],
                                "selected.marker.opacity": 1.0,
                                'unselected.marker.opacity': 0.2,
                                'marker.opacity': [opacities]
                            })
                        }
                    }
                })
                listeners_set = true
            }
        }
    }
}).observe(document.documentElement, {childList: true, subtree: true});

document.addEventListener('DOMSubtreeModified', function() {
    if (listeners_set && document.querySelectorAll("div.tab--selected")[0].innerText != "Stocks") {
        listeners_set = false;
    }
}, false);