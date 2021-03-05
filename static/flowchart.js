window.onload = function() {
    viewFlowchart();
};

function viewFlowchart() {

const program_map = {
    // 'nodes':[
    //     // level 1
    //     {
    //         'id': flowchart_courses[0].id,
    //         'courseid': flowchart_courses[0].ccode,
    //         'xcoord': 90,
    //         'ycoord': 10,
    //         'port': ['left', 'bottom', 'right']
    //     },
    //     {
    //         'id': flowchart_courses[2].id,
    //         'courseid': flowchart_courses[2].ccode,
    //         'xcoord': 270,
    //         'ycoord': 10,
    //         'port': ['left', 'bottom']
    //     },
    //     {
    //         'id': flowchart_courses[4].id,
    //         'courseid': flowchart_courses[4].ccode,
    //         'xcoord': 450,
    //         'ycoord': 10,
    //         'port': ['bottom']
    //     },
    //     {
    //         'id': flowchart_courses[6].id,
    //         'courseid': flowchart_courses[6].ccode,
    //         'xcoord': 630,
    //         'ycoord': 10,
    //         'port': []
    //     },
    //     {
    //         'id': flowchart_courses[8].id,
    //         'courseid': flowchart_courses[8].ccode,
    //         'xcoord': 810,
    //         'ycoord': 10,
    //         'port': []
    //     },
    //     {
    //         'id': flowchart_courses[10].id,
    //         'courseid': flowchart_courses[10].ccode,
    //         'xcoord': 990,
    //         'ycoord': 10,
    //         'port': []
    //     },
    //
    //     // level 2
    //     {
    //         'id': flowchart_courses[12].id,
    //         'courseid': flowchart_courses[12].ccode,
    //         'xcoord': 90,
    //         'ycoord': 220,
    //         'port': ['top']
    //     },
    //     {
    //         'id': flowchart_courses[14].id,
    //         'courseid': flowchart_courses[14].ccode,
    //         'xcoord': 270,
    //         'ycoord': 220,
    //         'port': ['top', 'bottom']
    //     },
    //     {
    //         'id': flowchart_courses[15].id,
    //         'courseid': flowchart_courses[15].ccode,
    //         'xcoord': 450,
    //         'ycoord': 220,
    //         'port': []
    //     },
    //     {
    //         'id': flowchart_courses[16].id,
    //         'courseid': flowchart_courses[16].ccode,
    //         'xcoord': 630,
    //         'ycoord': 220,
    //         'port': []
    //     },
    //     {
    //         'id': flowchart_courses[17].id,
    //         'courseid': flowchart_courses[17].ccode,
    //         'xcoord': 810,
    //         'ycoord': 220,
    //         'port': ['bottom']
    //     },
    //     {
    //         'id': 12,
    //         'courseid': 'GED3002',
    //         'xcoord': 990,
    //         'ycoord': 220,
    //         'port': []
    //     },
    //
    //     // level 3
    //     {
    //         'id': flowchart_courses[18].id,
    //         'courseid': flowchart_courses[18].ccode,
    //         'xcoord': 90,
    //         'ycoord': 430,
    //         'port': ['left', 'top']
    //     },
    //     {
    //         'id': flowchart_courses[19].id,
    //         'courseid': flowchart_courses[19].ccode,
    //         'xcoord': 270,
    //         'ycoord': 430,
    //         'port': ['left', 'bottom']
    //     },
    //     {
    //         'id': flowchart_courses[20].id,
    //         'courseid': flowchart_courses[20].ccode,
    //         'xcoord': 450,
    //         'ycoord': 430,
    //         'port': ['top', 'right']
    //     },
    //     {
    //         'id': flowchart_courses[22].id,
    //         'courseid': flowchart_courses[22].ccode,
    //         'xcoord': 810,
    //         'ycoord': 430,
    //         'port': ['top']
    //     },
    //     {
    //         'id': 17,
    //         'courseid': 'GED3002',
    //         'xcoord': 990,
    //         'ycoord': 430,
    //         'port': []
    //     },
    //
    //     // level 4
    //     {
    //         'id': flowchart_courses[23].id,
    //         'courseid': flowchart_courses[23].ccode,
    //         'xcoord': 90,
    //         'ycoord': 640,
    //         'port': ['top']
    //     },
    //     {
    //         'id': flowchart_courses[24].id,
    //         'courseid': flowchart_courses[24].ccode,
    //         'xcoord': 270,
    //         'ycoord': 640,
    //         'port': ['top']
    //     },
    //     {
    //         'id': flowchart_courses[25].id,
    //         'courseid': flowchart_courses[25].ccode,
    //         'xcoord': 450,
    //         'ycoord': 640,
    //         'port': ['top']
    //     },
    //     {
    //         'id': flowchart_courses[26].id,
    //         'courseid': flowchart_courses[26].ccode,
    //         'xcoord': 630,
    //         'ycoord': 640,
    //         'port': ['top']
    //     },
    // ],
    'nodes':[
        // level 1
        {
            'id': flowchart_courses[0].id,
            'courseid': flowchart_courses[0].ccode,
            'xcoord': 90,
            'ycoord': 10,
            'port': ['left', 'bottom', 'right']
        },
        {
            'id': flowchart_courses[1].id,
            'courseid': flowchart_courses[1].ccode,
            'xcoord': 270,
            'ycoord': 10,
            'port': ['left', 'bottom']
        },
        {
            'id': flowchart_courses[2].id,
            'courseid': flowchart_courses[2].ccode,
            'xcoord': 450,
            'ycoord': 10,
            'port': ['bottom']
        },
        {
            'id': flowchart_courses[3].id,
            'courseid': flowchart_courses[3].ccode,
            'xcoord': 630,
            'ycoord': 10,
            'port': []
        },
        {
            'id': flowchart_courses[4].id,
            'courseid': flowchart_courses[4].ccode,
            'xcoord': 810,
            'ycoord': 10,
            'port': []
        },
        {
            'id': flowchart_courses[5].id,
            'courseid': flowchart_courses[5].ccode,
            'xcoord': 990,
            'ycoord': 10,
            'port': []
        },

        // level 2
        {
            'id': flowchart_courses[6].id,
            'courseid': flowchart_courses[6].ccode,
            'xcoord': 90,
            'ycoord': 220,
            'port': ['top']
        },
        {
            'id': flowchart_courses[7].id,
            'courseid': flowchart_courses[7].ccode,
            'xcoord': 270,
            'ycoord': 220,
            'port': ['top', 'bottom']
        },
        {
            'id': flowchart_courses[8].id,
            'courseid': flowchart_courses[8].ccode,
            'xcoord': 450,
            'ycoord': 220,
            'port': []
        },
        {
            'id': flowchart_courses[9].id,
            'courseid': flowchart_courses[9].ccode,
            'xcoord': 630,
            'ycoord': 220,
            'port': []
        },
        {
            'id': flowchart_courses[10].id,
            'courseid': flowchart_courses[10].ccode,
            'xcoord': 810,
            'ycoord': 220,
            'port': ['bottom']
        },
        {
            'id': 12,
            'courseid': 'GED3002',
            'xcoord': 990,
            'ycoord': 220,
            'port': []
        },

        // level 3
        {
            'id': flowchart_courses[11].id,
            'courseid': flowchart_courses[11].ccode,
            'xcoord': 90,
            'ycoord': 430,
            'port': ['left', 'top']
        },
        {
            'id': flowchart_courses[12].id,
            'courseid': flowchart_courses[12].ccode,
            'xcoord': 270,
            'ycoord': 430,
            'port': ['left', 'bottom']
        },
        {
            'id': flowchart_courses[13].id,
            'courseid': flowchart_courses[13].ccode,
            'xcoord': 450,
            'ycoord': 430,
            'port': ['top', 'right']
        },
        {
            'id': flowchart_courses[14].id,
            'courseid': flowchart_courses[14].ccode,
            'xcoord': 810,
            'ycoord': 430,
            'port': ['top']
        },
        {
            'id': 17,
            'courseid': 'GED3002',
            'xcoord': 990,
            'ycoord': 430,
            'port': []
        },

        // level 4
        {
            'id': flowchart_courses[15].id,
            'courseid': flowchart_courses[15].ccode,
            'xcoord': 90,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[16].id,
            'courseid': flowchart_courses[16].ccode,
            'xcoord': 270,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[17].id,
            'courseid': flowchart_courses[17].ccode,
            'xcoord': 450,
            'ycoord': 640,
            'port': ['top']
        },
        {
            'id': flowchart_courses[18].id,
            'courseid': flowchart_courses[18].ccode,
            'xcoord': 630,
            'ycoord': 640,
            'port': ['top']
        },
    ],
    // prerequisite links
    'links': [
        {
            'source': {
                'id': prerequisite_links[4].source_id,
                'port': 'left'
            },
            'target': {
                'id': prerequisite_links[4].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[0].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[0].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[5].source_id,
                'port': 'right'
            },
            'target': {
                'id': prerequisite_links[5].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[6].source_id,
                'port': 'left'
            },
            'target': {
                'id': prerequisite_links[6].target_id,
                'port': 'left'
            }
        },
        {
            'source': {
                'id': prerequisite_links[1].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[1].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[2].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[2].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[3].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[3].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[7].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[7].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[8].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[8].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[9].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[9].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[10].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[10].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[11].source_id,
                'port': 'bottom'
            },
            'target': {
                'id': prerequisite_links[11].target_id,
                'port': 'top'
            }
        },
        {
            'source': {
                'id': prerequisite_links[12].source_id,
                'port': 'right'
            },
            'target': {
                'id': prerequisite_links[12].target_id,
                'port': 'top'
            }
        }
    ]
}

var electives = [];

// set grades and course info such as prof
for (var i = 0; i < program_map.nodes.length; i++) {
    for (var g = 0; g < student_results.length; g++) {
        if(program_map.nodes[i].courseid == student_results[g].ccode) {
            program_map.nodes[i].grade = student_results[g].grade;
            program_map.nodes[i].mapid = student_results[g].mapid;
            program_map.nodes[i].title = student_results[g].coursename;
            program_map.nodes[i].gid = student_results[g].gid;
            program_map.nodes[i].prof = student_results[g].prof;
            program_map.nodes[i].term = student_results[g].term;
            program_map.nodes[i].fcomment = student_results[g].fcomment;
            program_map.nodes[i].rcomment = student_results[g].rcomment;
            //console.log(program_map.nodes[i].grade);
        }
    }
}

for (var g = 0; g < student_results.length; g++) {
        if (student_results[g].id == null) {
            //console.log(student_results[g].ccode);

            if (student_results[g].ccode !='MAT8001' && student_results[g].ccode !='MAD9010.00') {
                electives.push(student_results[g]);
            }
        }
    }

var elective_options = [];
for (var i = 0; i < program_map.nodes.length; i++) {
    if (program_map.nodes[i].courseid === 'GED3002') {
        elective_options.push(program_map.nodes[i]);
    }
}

if (electives.length == 1 ) {
    console.log(electives[0]);
    elective_options[0].grade = electives[0].grade;
    elective_options[0].mapid = electives[0].mapid;
    elective_options[0].gid = electives[0].gid;
    elective_options[0].title = electives[0].coursename;
    elective_options[0].gedcode = electives[0].ccode;
    elective_options[0].prof = electives[0].prof;
    elective_options[0].term = electives[0].term;
    elective_options[0].fcomment = electives[0].fcomment;
    elective_options[0].rcomment = electives[0].rcomment;
}
else if (electives.length == 2) {
    elective_options[0].grade = electives[0].grade;
    elective_options[0].mapid = electives[0].mapid;
    elective_options[0].gid = electives[0].gid;
    elective_options[0].title = electives[0].coursename;
    elective_options[0].gedcode = electives[0].ccode;
    elective_options[0].prof = electives[0].prof;
    elective_options[0].term = electives[0].term;
    elective_options[0].fcomment = electives[0].fcomment;
    elective_options[0].rcomment = electives[0].rcomment;

    elective_options[1].grade = electives[1].grade;
    elective_options[1].mapid = electives[1].mapid;
    elective_options[1].gid = electives[1].gid;
    elective_options[1].title = electives[1].coursename;
    elective_options[1].gedcode = electives[1].ccode;
    elective_options[1].prof = electives[1].prof;
    elective_options[1].term = electives[1].term;
    elective_options[1].fcomment = electives[1].fcomment;
    elective_options[1].rcomment = electives[1].rcomment;
}

// window.onload = function() {
//     viewFlowchart();
// };

// function viewFlowchart() {

// graph: contains a reference to all components of your diagram
// graph is a model holding all cells (elements/links) which are stored in property 'cells'
var graph = new joint.dia.Graph;

joint.setTheme('modern');

// paper: responsible for rendering the graph
var paper = new joint.dia.Paper({
            el: $('div#flowchart'),
            model: graph,
            width: $('div#flowchart').width(),
            height: $('div#flowchart').height(),
            gridSize: 10,
            //drawGrid: true,

});



// custom shape
joint.shapes.basic.CourseBox = joint.shapes.basic.Generic.extend({

    markup: [{
        tagName: 'rect',
        selector: 'box',
    }, {
        tagName: 'text',
        selector: 'courseCode'
    }, {
        tagName: 'text',
        selector: 'grade'
    }, {
        tagName: 'image',
        selector: 'editIcon'
    }, {
        tagName: 'image',
        selector: 'infoIcon'
    }],

    defaults: joint.util.defaultsDeep({

        type: 'basic.CourseBox',
        size: { width: 120, height: 110 },
        attrs: {
            'box': {
                fill: '#9A9A9A', stroke: '#9A9A9A', width: 120, height: 110,
                rx: 10,
                ry: 10,
                filter: {
                    name: 'dropShadow',
                    args: {
                        dx: 4,
                        dy: 4,
                        blur: 3
                    }
                },
                cursor: 'default'
            },
            'courseCode': { 'cursor': 'default', 'font-size': 16, 'font-weight': 'bold', text: '', 'ref-x': .5, 'ref-y': 30, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#FAFAD2' },
            'grade': { 'cursor': 'default', 'font-size': 16, 'font-weight': 'bold', text: '', 'ref-x': .5, 'ref-y': 60, ref: 'box', 'y-alignment': 'middle', 'x-alignment': 'middle', fill: '#ffffff' },
            'editIcon': { 'xlink:href': '', 'ref-x': .75, 'ref-y': 78, ref: 'box', width: 25, height: 28, cursor: 'default'},
            'infoIcon': { 'xlink:href': '', 'ref-x': 5, 'ref-y': 76, ref: 'box', width: 30, height: 30, cursor: 'default'}
        },
        // define port groups
    ports: {
        groups: {
            'left': {
                position: {
                    name: 'left'
                },
                attrs: {
                    circle: { fill: '#000000', r: 0.2, magnet: true}
                }
            },
            'bottom': {
                position: {
                    name: 'bottom'
                },
                attrs: {
                    circle: { fill: '#000000', r: 0.2, magnet: true}
                }
            },
            'right': {
                position: {
                    name: 'right'
                },
                attrs: {
                    circle: { fill: '#000000', r: 0.2, magnet: true}
                }
            },
            'top': {
                position: {
                    name: 'top'
                },
                attrs: {
                    circle: { fill: '#000000', r:0.2, magnet: true}
                }
            }
        }

    }

    }, joint.shapes.basic.Generic.prototype.defaults)
});




//checkboxs
var viewChecked = document.getElementById("view").checked;
var genEdChecked = document.getElementById("genEd").checked;

var courseList = program_map.nodes;
var prereqlinks = program_map.links;
var i;
var createdCourses = [];
var portsides = ['top', 'right', 'bottom', 'left'];

// loop through course list to create shape for each
var second = false;
for (i=0; i < courseList.length; i++) {
    var code = null;
    if (second == false && courseList[i].courseid === 'GED3002') {
        if(elective_options[0].gedcode == undefined){
            code = courseList[i].courseid;
        }
        else{
            code = elective_options[0].gedcode;
        }
        second = true;
    }
    else if (second == true && courseList[i].courseid === 'GED3002') {
        if(elective_options[1].gedcode == undefined){
            code = courseList[i].courseid;
        }
        else{
            code = elective_options[1].gedcode;
        }
    }
    else{
        code = courseList[i].courseid;
    }
    var course = new joint.shapes.basic.CourseBox({
    position: { x: courseList[i].xcoord, y: courseList[i].ycoord },
    size: { width: 120, height: 110 },
    id: courseList[i].id,
    attrs: {
        // courseCode: { text: courseList[i].courseid},
        courseCode: { text: code},
    }
    
});
    // if genEdChecked checkbox not checked, no GenEds
    if ((courseList[i].id == 12 || courseList[i].id == 17) && genEdChecked == false){
        course.attr('box/display', 'none');
        course.attr('courseCode/display', 'none');
        course.attr('grade/display', 'none');
        course.attr('infoIcon/display', 'none');
        course.attr('editIcon/display', 'none');
    }

    // if no grade, don't display
    if (courseList[i].grade === "" || courseList[i].grade == undefined) {
        course.attr('grade/display', 'none');
        course.attr('courseCode/fill', '#ffffff');
    }
    else {
        course.attr('grade/text', 'Grade: '+ courseList[i].grade);

        if (courseList[i].grade == "F " || courseList[i].grade == "F") {
            // course.attr('box/fill', '#176629');
            // course.attr('box/stroke', '#176629');
            course.attr('box/fill', '#ff4d4d');
            course.attr('box/stroke', '#ff4d4d');
        }
        else {
            course.attr('box/fill', '#28A745');
            course.attr('box/stroke', '#28A745');
            // course.attr('box/fill', '#47539b');
            // course.attr('box/stroke', '#47539b');
        }

        course.attr('infoIcon/xlink:href', '/static/info-icon.png');
        course.attr('infoIcon/event', 'element:info');
        course.attr('infoIcon/cursor', 'pointer');
        if (admin_session == true) {
            course.attr('editIcon/xlink:href', '/static/edit-icon.png');
            course.attr('editIcon/event', 'element:edit');
            course.attr('editIcon/cursor', 'pointer');
        }
    }

    // add ports
    for (var s=0; s < portsides.length; s++) {
        for (var p=0; p < courseList[i].port.length; p++) {
            if (courseList[i].port[p] === portsides[s]) {
                course.addPort({group: portsides[s], magnet: true, attrs: {cursor: 'default'}});
            }
        }
    }


    createdCourses.push(course);
    course.addTo(graph);
}

// if viewChecked checkbox not checked, no Lines(links)
if(viewChecked == true) {
// add links
for (var l=0; l < prereqlinks.length; l++) {
    var link = new joint.shapes.standard.Link({
        source: prereqlinks[l].source,
        target: prereqlinks[l].target,
        connector: {name: 'rounded'},
        router: {
            name: 'manhattan',
            args: {
                step: 15,
                startDirections: [prereqlinks[l].source.port],
                endDirections: [prereqlinks[l].target.port],
                maximumLoops: 300
            }
        },
        attrs: {
            line: {
                strokeWidth: 4,
                stroke: '#000000',
                cursor: 'default'
            }
        }
    });

    link.addTo(graph);
}
}

// prevent moving shapes
// paper.setInteractivity({elementMove: false});


// paper event edit edit
paper.on('element:edit', function(elementView, evt, x, y) {
        $('p#editGradeError').text('');
        var getGrade;
        var getCourseId;
        var getMapid;
        var getTitle;
        var getName;
        var getGid;
        var getFcomment = "";
        var getRcomment = "";
        var k;
        var j;
        for(k=0; k<courseList.length; k++){
            if(courseList[k].id === elementView.model.id) {
                getGrade = courseList[k].grade;
                //getCourseId = courseList[k].courseid;
                getMapid = courseList[k].mapid;
                getTitle = courseList[k].title;
                getName = courseList[k].studentname;
                getNum = courseList[k].studentnum;
                getGid = courseList[k].gid;

                // show faculty comment if there is one, otherwise comment field is blank and editable
                if (courseList[k].fcomment != "") {
                    getFcomment = courseList[k].fcomment;
                    $('input#editcourseFcomment').val(getFcomment);
                }
                else {
                    getFcomment = "";
                    $('input#editcourseFcomment').val(getFcomment);
                }

                // show review comment if there is one, otherwise comment field is blank and editable
                if (courseList[k].rcomment != "") {
                    getRcomment = courseList[k].rcomment;
                    $('input#editcourseRcomment').val(getRcomment);
                }
                else {
                    getRcomment = "";
                    $('input#editcourseRcomment').val(getRcomment);
                }


                if (elementView.model.id === 12) {
                    for (j=0; j < elective_options.length; j++) {
                        if (courseList[k].mapid === elective_options[j].mapid) {
                            getCourseId = elective_options[j].gedcode;
                        }
                    }
                }
                else if (elementView.model.id === 17) {
                    for (j=0; j < elective_options.length; j++) {
                        if (courseList[k].mapid === elective_options[j].mapid) {
                            getCourseId = elective_options[j].gedcode;
                        }
                    }
                }
                else {
                    getCourseId = courseList[k].courseid;
                }
            }
        }


        // edit modal
        $('#editGradeFlowchart').modal('show');
        $('input#courseCode').val(getCourseId);
        $('input#gradeID').val(getGid);
        $('input#courseTitle').val(getTitle);
        $('input#inputGradeFlowchart').val(getGrade);
        $('input#mapid').val(getMapid);


    }
);

// hide div of faculty comment in info modal
$('div#fcomment').hide();

// hide div of review comment in info modal
$('div#rcomment').hide();


// paper event info modal
paper.on('element:info', function(elementView, evt, x, y) {
        var getGrade;
        var getCourseId;
        var getMapid;
        var getTitle;
        var getName;
        var getNum;
        var getGid;
        var getProf;
        var getTerm;
        var getFcomment = "";
        var getRcomment = "";
        var k;
        var j;
        for(k=0; k<courseList.length; k++){
            if(courseList[k].id === elementView.model.id) {
                getGrade = courseList[k].grade;
                //getCourseId = courseList[k].courseid;
                getMapid = courseList[k].mapid;
                getTitle = courseList[k].title;
                getName = courseList[k].studentname;
                getNum = courseList[k].studentnum;
                getGid = courseList[k].gid;
                getProf= courseList[k].prof;
                getTerm = courseList[k].term;

                if (courseList[k].fcomment != "") {
                    $('div#fcomment').show();
                    getFcomment = courseList[k].fcomment;
                    $('input#infocourseFcomment').val(getFcomment);
                }
                else {
                    getFcomment = "";
                    $('input#infocourseFcomment').val(getFcomment);
                    $('div#fcomment').hide();
                }


                if (courseList[k].rcomment != "") {
                    $('div#rcomment').show();
                    getRcomment = courseList[k].rcomment;
                    $('input#infocourseRcomment').val(getRcomment);
                }
                else {
                    getRcomment = "";
                    $('input#infocourseRcomment').val(getRcomment);
                    $('div#rcomment').hide();
                }


                if (elementView.model.id === 12) {
                    for (j=0; j < elective_options.length; j++) {
                        if (courseList[k].mapid === elective_options[j].mapid) {
                            getCourseId = elective_options[j].gedcode;
                        }
                    }
                }
                else if (elementView.model.id === 17) {
                    for (j=0; j < elective_options.length; j++) {
                        if (courseList[k].mapid === elective_options[j].mapid) {
                            getCourseId = elective_options[j].gedcode;
                        }
                    }
                }
                else {
                    getCourseId = courseList[k].courseid;
                }
            }
        }



        // info modal
        $('#infoFlowchart').modal('show');
        $('input#infocourseCode').val(getCourseId);
        $('input#infocourseTitle').val(getTitle);
        $('input#mapid').val(getMapid);
        $('input#infocourseProf').val(getProf);
        $('input#infocourseTerm').val(getTerm);
        $('input#infocourseGrade').val(getGrade);
        $('input#infoGradeID').val(getGid);

    }

  
);
}
