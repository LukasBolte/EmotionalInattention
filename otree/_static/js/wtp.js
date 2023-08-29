"use strict";

function drawWTP(parameters){
    this.leftHeader=parameters.leftHeader
    this.rightHeader=parameters.rightHeader
    this.leftBonus=parameters.leftBonus
    this.rightBonus=parameters.rightBonus
    this.varname=parameters.varname
    this.root=parameters.root
    this.color_switched=parameters.color_switched
    this.hidden_fields_name=parameters.hidden_fields_name
    this.playerID=parameters.playerID
    this.tdList={};
    this.selectedCutoff;
    this.cutoffHistory=[];

    this.leftDiv;
    this.rightDiv;

    

    var modal_div=document.createElement("div");
    modal_div.innerHTML=`
    <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="confirmModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
            <div class="modal-body" id="confirm_modal_text_id">
                <p class="pb-0 mb-0">Dummy Text</p>
            </div>
            <div class="modal-footer">
                <button type="button" data-bs-dismiss="modal" class="btn btn-secondary">Change answers</button>
                <button id="id_button_end_task" style="float: right" class="btn btn-primary btn-large">Confirm</button>
            </div>
            </div>
        </div>
    </div>`


    document.getElementById(this.root).appendChild(modal_div);



    this.drawChoices = function(base,leftHeader,rightHeader,leftBonus,rightBonus){
        var table=document.createElement("table");
        table.setAttribute("id","id_"+this.varname)
        table.className="table table-sm table-hover mx-0 px-0 mb-0";
        table.style.backgroundColor = 'navajowhite';
        table.style.pointerEvents = '';
      
        base.appendChild(table);
        //add header
        var thead=document.createElement("thead");
        table.appendChild(thead);
        var trHead=document.createElement("tr");
        thead.appendChild(trHead);
        //now column headers
        var thHead=document.createElement("th");
        thHead.className="text-center";
        thHead.setAttribute("scope","col");
        thHead.style.width="35%";
        var text=document.createTextNode(leftHeader);
        thHead.appendChild(text);
        trHead.appendChild(thHead);
        
        var thHead=document.createElement("th");
        thHead.setAttribute("scope","col");
        thHead.style.width="20%";
        trHead.appendChild(thHead);

        var thHead=document.createElement("th");
        thHead.setAttribute("scope","col");
        var text=document.createTextNode(rightHeader);
        thHead.appendChild(text);
        thHead.className="text-center";
        thHead.style.width="35%";
        trHead.appendChild(thHead);
        //create body
        var tbody=document.createElement("tbody");
        tbody.addEventListener("mouseleave", this.unhighlight.bind(this));
        
        table.appendChild(tbody);
        var counter=0;
        for(let i=0;i<leftBonus.length;i++){
            var tr=document.createElement("tr");
            tr.setAttribute('height',"15px");
            if ((leftBonus[i]=="Get/Pay $0.00") || (rightBonus[i]=="Get/Pay $0.00")){
                tr.className='border-5 border-danger'  
            };
   
            this.tdList[i]=[];
            tbody.appendChild(tr);
            //left choice
            var td=document.createElement("td");
            td.className="text-center p-0";
            var text=document.createTextNode(leftBonus[i]);
            td.appendChild(text);
            td.setAttribute("cutoff","left:"+i);
            
            tr.appendChild(td);
            this.tdList[i].push(td);
            td.addEventListener("click", this.selectCutoff.bind(this));
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            //middle OR
            var td=document.createElement("td");
            td.className="text-center p-0";
            text=document.createTextNode("OR");
            td.setAttribute("cutoff","middle:"+i);
            td.appendChild(text);
            tr.appendChild(td);
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            //right choice
            var td=document.createElement("td");
            td.className="text-center p-0";
            text=document.createTextNode(rightBonus[i]);
            td.appendChild(text);
            td.setAttribute("cutoff","right:"+i);
            tr.appendChild(td);        
            this.tdList[i].push(td);
            td.addEventListener("click", this.selectCutoff.bind(this));
            td.addEventListener("mouseenter", this.highlightSelection.bind(this));
            counter++;
        }
    }


    this.highlight = function(cutoff,color){
        var choiceFrags=cutoff.split(':');
        var cutoffNum=parseFloat(choiceFrags[1]);
        for(var c in this.tdList){
            var cf=parseFloat(c);
            $(this.tdList[c][0]).removeClass("orange");
            $(this.tdList[c][0]).removeClass("darkorange");
            $(this.tdList[c][1]).removeClass("orange");
            $(this.tdList[c][1]).removeClass("darkorange");
            var color_dummy = 0;
            if (this.color_switched) {
                color_dummy = 1;
                console.log('color switched')
            };

            if (cf<cutoffNum){
                $(this.tdList[c][color_dummy]).addClass(color);
            }
            if (cf>cutoffNum){
                $(this.tdList[c][1-color_dummy]).addClass(color);
            }
            if (cf==cutoffNum){
                switch(choiceFrags[0]){
                    case "left":
                        $(this.tdList[c][0]).addClass(color);
                        break;
                    case "middle":
                        break;
                    case "right":
                        $(this.tdList[c][1]).addClass(color);
                        break;
                }
            }
        }    
    }
    
    this.unhighlight = function(){
        if (this.selectedCutoff){
            return;
        }
        for(var c in this.tdList){
            $(this.tdList[c][0]).removeClass("orange");
            $(this.tdList[c][1]).removeClass("orange");
            $(this.tdList[c][0]).removeClass("darkorange");
            $(this.tdList[c][1]).removeClass("darkorange");
        }
    }
    
    this.showNext=function(){
        var nextButton=document.getElementById("id_next_button");
        if (nextButton){
            nextButton.style.display="";
        }
    }
    
    this.selectCutoff = function(e){
        if (this.selectedCutoff){
            this.cutoffHistory.push(this.selectedCutoff);
        }
        var cutoff=e.target.getAttribute("cutoff");
        this.selectedCutoff=cutoff;
        this.highlight(cutoff,"darkorange");
        //save data in hidden field
        document.getElementById(this.varname).value=JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff});   
        
        var keyName=this.playerID+":"+this.root+":"+this.varname;
        localStorage.setItem(keyName,JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff}));
        console.log(document.getElementById(this.varname).value);  
        //make the oTree next button appear if present
        setTimeout(this.showNext,2000);

        this.drawExplainer();
    }
    
    this.highlightSelection = function(e){
        e.target.style.cursor = "pointer";
        if (this.selectedCutoff){
            return;
        }
        var cutoff=e.target.getAttribute("cutoff");
        this.highlight(cutoff,"orange");
    }



    //// starting
    //storage functions
    this.load=function(){
        console.log('I am loading')
        var keyName=this.playerID+":"+this.root+":"+this.varname;
        var savedValue=localStorage.getItem(keyName); 
        //console.log(savedValue);
        if (savedValue!=undefined){
            var output=JSON.parse(savedValue);
            this.selectedCutoff = output["cutoff"]
            this.cutoffHistory = output["history"]
            console.log(this.selectedCutoff)
            this.highlight(this.selectedCutoff,"darkorange");
            document.getElementById(this.varname).value=JSON.stringify({"history":this.cutoffHistory,"cutoff":this.selectedCutoff});   
        }
    }
    //// ending


    var hiddenDiv = document.getElementById(this.hidden_fields_name);
    var hiddenField=document.createElement("input");
    hiddenDiv.appendChild(hiddenField);
    hiddenField.setAttribute("type","hidden");
    hiddenField.setAttribute("name",this.varname);
    hiddenField.setAttribute("id",this.varname); 
    //draw game  
    var container=document.createElement("div");
    container.className="container";
    document.getElementById(this.root).appendChild(container);
    var row=document.createElement("div");
    row.className="row";
    container.appendChild(row);
    this.leftDiv=document.createElement("div");
    this.leftDiv.className="col-2 px-0";
    this.leftDiv.innerHTML="&nbsp;";
    row.appendChild(this.leftDiv);
    this.midDiv=document.createElement("div");
    this.midDiv.className="col-8 px-0 mx-0";
    row.appendChild(this.midDiv);
    this.rightDiv=document.createElement("div");
    this.rightDiv.className="col-2 px-0";
    this.rightDiv.innerHTML="&nbsp;";
    row.appendChild(this.rightDiv);
    this.drawChoices(this.midDiv,this.leftHeader,this.rightHeader,this.leftBonus,this.rightBonus);
    this.load();

    console.log(document.getElementById(this.varname).value,'my value')
    this.drawExplainer = function(){
        if (this.selectedCutoff!=undefined){
            
            console.log(this.selectedCutoff,'my cutoff')
            var choiceFrags=this.selectedCutoff.split(':');
            var cutoffNum=parseFloat(choiceFrags[1])+1;

            var multipler = cutoffNum;
            if (choiceFrags[0] == 'right') {
                multipler += 1;
            }

            var tdheight = parseFloat(window.getComputedStyle(this.tdList[0][0]).height)


            var base = this.rightDiv;
            base.innerHTML = '';
            var div=document.createElement("div");
            base.appendChild(div);

            div.className="text-center p-2";


            console.log('my Multiplier',multipler)

            var switch_row = multipler - 2; 
            console.log('my switch row',switch_row,this.tdList)
            if ((switch_row >= 0) && (switch_row < this.leftBonus.length-1)) {
                var text = 'I prefer completing the job over ' + this.rightBonus[switch_row+1] + ' but I prefer ' + this.rightBonus[switch_row] + ' over completing the job';
            } else if (switch_row < 0) {
                var text = 'I prefer completing the job over ' + this.rightBonus[0];
            } else {
                console.log('I am here',this.rightBonus, this.rightBonus.length-1)
                var text = 'I prefer ' + this.rightBonus[this.rightBonus.length-1] + ' over completing the job';
            }

            text = text.replaceAll("Pay", "paying");
            text = text.replaceAll("Get", "getting");

            var modal_text = document.getElementById("confirm_modal_text_id")
            modal_text.innerHTML = ''
            var p1 = document.createElement("p");
            
            p1.innerHTML = 'You chose: '
            
            
            modal_text.appendChild(p1);

            var ptext = document.createElement("p");
            ptext.innerHTML = '<i>' + text + '</i>';
            ptext.className = 'text-center'
            modal_text.appendChild(ptext);
            var p2 = document.createElement("p");
            p2.className = "pb-0 mb-0";
            p2.innerHTML = 'Is this correct? Please confirm below.'
            modal_text.appendChild(p2);

            document.getElementById("next_button_id_de").disabled= false;
          
            
            // I prefer completing the task over " + this.leftBonus[i] + " but I prefer " + this.rightBonus[i] over completing the task"
            div.innerHTML=text;
            div.style.width=window.getComputedStyle(base).width;
            var h=parseFloat(window.getComputedStyle(div).height);
            div.style.position="relative";

            var tbody = document.getElementById("id_wtp").getElementsByTagName("tbody")[0];
            var tbody_height=parseFloat(window.getComputedStyle(tbody).height);
            console.log('mycurrent top',div.style.top)

            console.log('my Multiplier',multipler)

            var adjusted_offset = -h/2+multipler*tdheight
            var max_offset = parseFloat(window.getComputedStyle(this.rightDiv).height) - h
            adjusted_offset = Math.min(adjusted_offset, max_offset)
            div.style.top=adjusted_offset+    "px";
            console.log('my multiplier: ',multipler)
        } else {
            var base = this.rightDiv;
            base.innerHTML = '';
            var div=document.createElement("div");
            base.appendChild(div);
            div.className="text-center p-2";
            div.innerHTML='Click on a row to input your choices!';
            div.style.width=window.getComputedStyle(base).width;
            var h=parseFloat(window.getComputedStyle(div).height);
            div.style.position="relative";

            var tbody = document.getElementById("id_wtp").getElementsByTagName("tbody")[0];
            var tbody_height=parseFloat(window.getComputedStyle(tbody).height);
            div.style.top=-h/2+tbody_height/2+    "px";
        }       
    }
    this.drawExplainer();


    this.drawArrows = function(){


        var table = document.getElementById("id_wtp");
        var thead = table.querySelector('thead');
        var tr = thead.querySelector('tr');

        var trHeight = window.getComputedStyle(tr).height

        trHeight = parseFloat(trHeight)

        var spacer_div = document.createElement("div")
        spacer_div.style.height = trHeight + 'px'
        spacer_div.style.width = '100%'



        var canvas = document.createElement("canvas");
        canvas.setAttribute("id","id_canvas");

        var window_height = parseFloat(window.getComputedStyle(this.leftDiv).height)
        canvas.setAttribute("width", window.getComputedStyle(this.leftDiv).width)
        canvas.setAttribute("height", (window_height - trHeight) + "px")

        console.log(window_height,trHeight)

        this.leftDiv.innerHTML='';
        this.leftDiv.appendChild(spacer_div);
        this.leftDiv.appendChild(canvas);
        var context = canvas.getContext("2d");

         // Save the initial context
        context.save();

    
        // Arrow line
        context.beginPath();
        context.moveTo(canvas.width/2, .45*canvas.height );
        context.lineTo(canvas.width/2, .2*canvas.height);
        context.lineWidth = 40;
        context.strokeStyle = "darkgreen";
        context.stroke();

        // Arrowhead
        context.moveTo(.3*canvas.width, .2*canvas.height);
        context.lineTo(.5*canvas.width, .1*canvas.height);
        context.lineTo(.7*canvas.width, .2*canvas.height);
        context.fillStyle = "darkgreen";
        context.fill();

        // Arrow line
        context.beginPath();
        context.moveTo(canvas.width/2, .55*canvas.height );
        context.lineTo(canvas.width/2, .8*canvas.height);
        context.lineWidth = 40;
        context.strokeStyle = "darkred";
        context.stroke();



        // Arrowhead
        context.moveTo(.3*canvas.width, .8*canvas.height);
        context.lineTo(.5*canvas.width, .9*canvas.height);
        context.lineTo(.7*canvas.width, .8*canvas.height);
       
        context.fillStyle = "darkred";

        context.fill();

        // Restore the initial context
        context.restore();

        // Text 1

        context.save();

        // Rotate the canvas context by -90 degrees for the second text
        context.rotate(-Math.PI / 2);

        // Text 1
        context.font = "bold 25px Arial"; // Larger font size
        context.textAlign = "center";
        context.fillText("I like the job", -.3*canvas.height,1/4*canvas.width);

        // Restore the saved context for future drawings
        context.restore();

        // Text 2

        context.save();

        // Rotate the canvas context by -90 degrees for the second text
        context.rotate(-Math.PI / 2);

        // Text 2
        context.font = "bold 25px Arial"; // Larger font size
        context.textAlign = "center";
        context.fillText("I don't like the job", -.7*canvas.height,1/4*canvas.width);

        // Restore the saved context for future drawings
        context.restore();


     
    }

    this.drawArrows();


}



// var drawExplainer=function(on_left,ymin,ymax,text){
//     var base=rightDiv;
//     if (on_left){
//         base=leftDiv;
//     }
//     $(base).empty();
//     var div=document.createElement("div");
//     base.appendChild(div);
//     div.innerHTML=text;
//     div.style.width=window.getComputedStyle(base).width;
//     var h=parseFloat(window.getComputedStyle(div).height);
//     div.style.position="absolute";
//     div.style.top=(-h/2+(ymin+ymax)/2)+"px";
// }

// var formatExplainer = function(rows,leftright){
//     if (rows==1){
//         return "If this row is selected for payment you are choosing the "+leftright+" option."
//     }
//     else{  
//         return "If one of these "+rows+" rows is selected for payment you are choosing the "+leftright+" option."
//     }
// }

this.highlight = function(cutoff,color){
    var choiceFrags=cutoff.split(':');
    var cutoffNum=parseFloat(choiceFrags[1]);
    for(var c in this.tdList){
        var cf=parseFloat(c);
        $(this.tdList[c][0]).removeClass("orange");
        $(this.tdList[c][0]).removeClass("darkorange");
        $(this.tdList[c][1]).removeClass("orange");
        $(this.tdList[c][1]).removeClass("darkorange");
        var color_dummy = 0;
        if (this.color_switched) {
            color_dummy = 1;
            console.log('color switched')
        };

        if (cf<cutoffNum){
            $(this.tdList[c][color_dummy]).addClass(color);
        }
        if (cf>cutoffNum){
            $(this.tdList[c][1-color_dummy]).addClass(color);
        }
        if (cf==cutoffNum){
            switch(choiceFrags[0]){
                case "left":
                    $(this.tdList[c][0]).addClass(color);
                    break;
                case "middle":
                    break;
                case "right":
                    $(this.tdList[c][1]).addClass(color);
                    break;
            }
        }
    }    
}
